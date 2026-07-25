"""
Appointment booking logic: slot conflict checks, lifecycle transitions
(approve/reject/cancel/reschedule), and walk-in token assignment.
"""

import secrets
from datetime import date, datetime, timedelta

from sqlalchemy.exc import IntegrityError

from smartcare.extensions import db
from smartcare.models.appointment import Appointment, AppointmentStatus
from smartcare.models.doctor import DoctorAvailability


class AppointmentConflictError(Exception):
    """Raised when a requested slot is already taken for that doctor."""


def is_slot_in_past(appointment_date, time_slot):
    """True if the given date/time-slot combination has already passed.
    Used both to filter the slot picker for today, and as a final
    server-side guard in book_appointment()/reschedule_appointment() —
    belt-and-suspenders against a stale page, manipulated request, or
    client clock skew slipping a past slot through the earlier checks."""
    if appointment_date < date.today():
        return True
    if appointment_date > date.today():
        return False
    try:
        start_str = time_slot.split(" - ")[0].strip()
        start_time = datetime.strptime(start_str, "%I:%M %p").time()
    except (ValueError, AttributeError, IndexError):
        return False
    return datetime.combine(appointment_date, start_time) <= datetime.now()


def is_slot_taken(doctor_id, appointment_date, time_slot, exclude_appointment_id=None):
    query = Appointment.query.filter_by(
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        time_slot=time_slot,
    ).filter(Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.APPROVED]))

    if exclude_appointment_id:
        query = query.filter(Appointment.id != exclude_appointment_id)

    return db.session.query(query.exists()).scalar()


def book_appointment(
    patient_id,
    doctor_id,
    department_id,
    appointment_date,
    time_slot,
    reason=None,
    created_by="self",
    consultation_type="in_person",
):
    if is_slot_in_past(appointment_date, time_slot):
        raise AppointmentConflictError("This date/time has already passed. Please choose a future slot.")

    # Fast-path check: catches the overwhelming majority of conflicts cheaply,
    # without even attempting a write.
    if is_slot_taken(doctor_id, appointment_date, time_slot):
        raise AppointmentConflictError("This time slot is already booked. Please choose another.")

    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        department_id=department_id,
        appointment_date=appointment_date,
        time_slot=time_slot,
        reason=reason,
        created_by=created_by,
        consultation_type=consultation_type,
        status=AppointmentStatus.PENDING,
    )
    db.session.add(appointment)

    try:
        db.session.commit()
    except IntegrityError:
        # True race condition: two requests both passed the check above at
        # nearly the same instant. The database's partial unique index
        # (see Appointment.__table_args__) is the final, authoritative
        # guard — it rejects the second insert, and we surface that as the
        # same friendly conflict error the caller already expects.
        db.session.rollback()
        raise AppointmentConflictError("This time slot is already booked. Please choose another.")

    return appointment


def cancel_appointment(appointment):
    appointment.status = AppointmentStatus.CANCELLED
    appointment.updated_at = datetime.utcnow()
    db.session.commit()
    return appointment


def reschedule_appointment(appointment, new_date, new_time_slot):
    if is_slot_in_past(new_date, new_time_slot):
        raise AppointmentConflictError("This date/time has already passed. Please choose a future slot.")

    if is_slot_taken(appointment.doctor_id, new_date, new_time_slot, exclude_appointment_id=appointment.id):
        raise AppointmentConflictError("The new time slot is already booked. Please choose another.")

    appointment.appointment_date = new_date
    appointment.time_slot = new_time_slot
    # Reschedules go back through approval rather than staying "approved"
    # or landing in a dead-end RESCHEDULED state with no action buttons —
    # the doctor may not be free at the new time, so the old approval
    # shouldn't silently carry over. This also re-surfaces the appointment
    # in the doctor's Pending Approvals queue automatically.
    appointment.status = AppointmentStatus.PENDING
    # Any previously-generated video link was tied to the old slot; clear
    # it so approve_appointment() generates a fresh one for the new time
    # rather than sending the patient a link for a slot that no longer exists.
    appointment.meeting_link = None
    appointment.updated_at = datetime.utcnow()

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise AppointmentConflictError("The new time slot is already booked. Please choose another.")

    return appointment


def approve_appointment(appointment):
    appointment.status = AppointmentStatus.APPROVED
    appointment.updated_at = datetime.utcnow()

    # Only generate a video link for online consultations, and only once
    # (so re-approving / re-saving never overwrites an already-shared link).
    if appointment.consultation_type == "online" and not appointment.meeting_link:
        appointment.meeting_link = generate_meeting_link(appointment.id)

    try:
        db.session.commit()
    except IntegrityError:
        # Approving could theoretically collide with another appointment
        # that raced into the same slot after this one was created as PENDING.
        db.session.rollback()
        raise AppointmentConflictError("This slot was booked by someone else in the meantime.")

    return appointment


def generate_meeting_link(appointment_id):
    """Builds a free Jitsi Meet room URL — no paid API, no signup needed.
    The random token makes the room unguessable by anyone who isn't sent
    this exact link, even though Jitsi rooms have no login."""
    token = secrets.token_urlsafe(8)
    return f"https://meet.jit.si/SmartCareX-{appointment_id}-{token}"


def reject_appointment(appointment):
    appointment.status = AppointmentStatus.REJECTED
    appointment.updated_at = datetime.utcnow()
    db.session.commit()
    return appointment


def mark_completed(appointment):
    appointment.status = AppointmentStatus.COMPLETED
    appointment.updated_at = datetime.utcnow()
    db.session.commit()
    return appointment


def next_token_number(doctor_id, appointment_date):
    """Assigns the next sequential token number for a doctor's queue on a given day."""
    last_token = (
        db.session.query(db.func.max(Appointment.token_number))
        .filter_by(doctor_id=doctor_id, appointment_date=appointment_date)
        .scalar()
    )
    return (last_token or 0) + 1


def register_walkin_appointment(patient_id, doctor_id, department_id, appointment_date, time_slot, reason=None):
    appointment = book_appointment(
        patient_id, doctor_id, department_id, appointment_date, time_slot, reason, created_by="reception"
    )
    appointment.token_number = next_token_number(doctor_id, appointment_date)
    db.session.commit()
    return appointment


def get_available_slots(doctor_id, appointment_date):
    """
    Builds the list of bookable time-slot strings for a doctor on a given
    date, derived from their recurring DoctorAvailability windows, split
    into slot_duration_minutes chunks, minus slots already taken.
    """
    day_of_week = appointment_date.weekday()  # 0=Monday ... 6=Sunday

    windows = DoctorAvailability.query.filter_by(
        doctor_id=doctor_id, day_of_week=day_of_week, is_active=True
    ).all()

    if not windows:
        return []

    taken_slots = {
        a.time_slot
        for a in Appointment.query.filter_by(doctor_id=doctor_id, appointment_date=appointment_date)
        .filter(Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.APPROVED]))
        .all()
    }

    slots = []
    for window in windows:
        current = datetime.combine(appointment_date, window.start_time)
        end = datetime.combine(appointment_date, window.end_time)
        step = timedelta(minutes=window.slot_duration_minutes)

        while current + step <= end:
            slot_label = f"{current.strftime('%I:%M %p')} - {(current + step).strftime('%I:%M %p')}"
            # For today's date, don't even offer times that have already gone.
            already_passed = appointment_date == date.today() and current <= datetime.now()
            if slot_label not in taken_slots and not already_passed:
                slots.append(slot_label)
            current += step

    return slots


def get_todays_appointments(doctor_id):
    return (
        Appointment.query.filter_by(doctor_id=doctor_id, appointment_date=datetime.utcnow().date())
        .order_by(Appointment.time_slot.asc())
        .all()
    )
import enum
from datetime import datetime

from smartcare.extensions import db


class AppointmentStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)

    appointment_date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)  # e.g. "10:00 AM - 10:15 AM"
    status = db.Column(db.Enum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False, index=True)
    reason = db.Column(db.Text)
    token_number = db.Column(db.Integer)  # assigned for walk-ins / same-day queue

    # "self" = patient booked online, "reception" = walk-in registered at desk
    created_by = db.Column(db.String(20), default="self", nullable=False)

    # "in_person" (default — covers walk-ins too) or "online" (video consultation)
    consultation_type = db.Column(db.String(20), default="in_person", nullable=False)
    # Auto-generated free Jitsi Meet link, filled in only when an "online"
    # appointment gets approved by the doctor (see approve_appointment()).
    meeting_link = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")
    department = db.relationship("Department", back_populates="appointments")

    prescription = db.relationship("Prescription", back_populates="appointment", uselist=False, cascade="all, delete-orphan")
    bill = db.relationship("Bill", back_populates="appointment", uselist=False)

    __table_args__ = (
        # Database-level guarantee against double-booking: only one PENDING or
        # APPROVED appointment can exist for a given doctor + date + time slot,
        # even if two booking requests arrive at the exact same instant. This
        # is a partial unique index — cancelled/rejected/completed appointments
        # don't count, so a slot frees up again once its old booking is resolved.
        # Note: SQLAlchemy's Enum column stores the Python enum MEMBER NAME
        # ("PENDING"/"APPROVED"), not its .value ("pending"/"approved").
        db.Index(
            "uq_doctor_date_slot_active",
            "doctor_id",
            "appointment_date",
            "time_slot",
            unique=True,
            sqlite_where=db.text("status IN ('PENDING', 'APPROVED')"),
            postgresql_where=db.text("status IN ('PENDING', 'APPROVED')"),
        ),
    )

    def __repr__(self):
        return f"<Appointment #{self.id} {self.appointment_date} {self.status.value}>"
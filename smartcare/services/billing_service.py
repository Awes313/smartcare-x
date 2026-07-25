from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

from smartcare.extensions import db
from smartcare.models.billing import BILL_DUE_DAYS, Bill, BillItem, Payment

DEFAULT_TAX_RATE = Decimal("0.05")


def _round2(value):
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def create_bill(patient_id, generated_by_user_id, line_items, appointment_id=None, prescription_id=None, tax_rate=DEFAULT_TAX_RATE, with_due_date=False, channel="counter"):
    bill = Bill(
        patient_id=patient_id,
        appointment_id=appointment_id,
        prescription_id=prescription_id,
        generated_by=generated_by_user_id,
        channel=channel,
    )
    if with_due_date:
        bill.due_date = datetime.utcnow() + timedelta(days=BILL_DUE_DAYS)

    subtotal = Decimal("0.00")
    for line in line_items:
        quantity = int(line["quantity"])
        unit_price = Decimal(str(line["unit_price"]))
        line_total = _round2(unit_price * quantity)
        subtotal += line_total

        bill.items.append(
            BillItem(
                description=line["description"],
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            )
        )

    tax = _round2(subtotal * tax_rate)
    bill.subtotal = subtotal
    bill.tax = tax
    bill.total = subtotal + tax
    bill.status = "unpaid"

    db.session.add(bill)
    db.session.commit()
    return bill


def record_payment(bill, amount, method="cash"):
    payment = Payment(amount=_round2(amount), method=method)
    # Appending through the relationship (instead of setting bill_id
    # directly) keeps bill.payments in sync in-memory immediately, so the
    # balance_due/status check right below always sees this payment —
    # avoids a stale-collection bug where the bill's status could get
    # stuck on "unpaid" even after the full amount was paid.
    bill.payments.append(payment)
    db.session.add(payment)
    db.session.flush()

    if bill.balance_due <= Decimal("0.00"):
        bill.status = "paid"
    elif bill.amount_paid > Decimal("0.00"):
        bill.status = "partial"

    db.session.commit()
    return payment


def mark_refund_pending(appointment):
    """Called when an appointment gets cancelled/rejected. Handles its
    consultation-fee bill (if any) according to what was actually paid:
      - "paid"            -> flag for refund (money already changed hands,
                              mirrors real payment gateways: cancelling
                              never triggers an instant cash reversal)
      - "unpaid"/"partial" -> void the bill outright, since no fee should
                              ever be collected for a visit that won't
                              happen. Without this, an unpaid bill for a
                              cancelled appointment would sit forever in
                              reception's Billing list, risking staff
                              collecting payment for a cancelled visit.
    No-op if there's no bill at all."""
    bill = appointment.bill
    if not bill:
        return

    if bill.status == "paid":
        bill.status = "refund_pending"
    elif bill.status in ("unpaid", "partial"):
        bill.status = "void"

    db.session.commit()


def mark_bill_refunded(bill):
    """Called by an admin once the refund has actually been processed
    outside the app (e.g. via the Razorpay dashboard) — this is a manual
    confirmation step, not an automatic one, since only finance/admin can
    verify money actually moved."""
    bill.status = "refunded"
    db.session.commit()


def get_unpaid_bills(patient_id=None, channel=None):
    """Used by the PATIENT's own dashboard. Passing channel explicitly
    filters to just that collection path. Counter bills are intentionally
    excluded when channel="online" is passed, since a patient paying those
    via Razorpay while reception ALSO collects cash/card for the same bill
    would be a double payment."""
    query = Bill.query.filter(Bill.status.in_(["unpaid", "partial"]))
    if patient_id:
        query = query.filter_by(patient_id=patient_id)
    if channel:
        query = query.filter_by(channel=channel)
    return query.order_by(Bill.created_at.desc()).all()


def get_receptionist_unpaid_bills():
    """Unpaid bills reception is actually allowed to collect cash/card
    payment for — i.e. counter-channel bills only. Online-channel bills
    (online booking consultation fees, online-booked prescription medicine
    bills) are deliberately excluded — those are Razorpay-only by design,
    so reception never gets a second, conflicting way to collect the same
    charge. Voided bills (see mark_refund_pending) are also excluded since
    their status is no longer "unpaid"/"partial"."""
    return (
        Bill.query.filter(Bill.status.in_(["unpaid", "partial"]))
        .filter_by(channel="counter")
        .order_by(Bill.created_at.desc())
        .all()
    )


def get_refund_pending_bills(patient_id=None):
    query = Bill.query.filter_by(status="refund_pending")
    if patient_id:
        query = query.filter_by(patient_id=patient_id)
    return query.order_by(Bill.created_at.desc()).all()


def get_bills_needing_reminder():
    """Bills that are unpaid, have a due date, haven't been reminded yet,
    and are within 1 day of (or past) their due date — used by the
    scheduled reminder job so it doesn't email every unpaid bill daily,
    only ones actually approaching/past the deadline."""
    cutoff = datetime.utcnow() + timedelta(days=1)
    return (
        Bill.query.filter(Bill.status.in_(["unpaid", "partial"]))
        .filter(Bill.due_date.isnot(None))
        .filter(Bill.due_date <= cutoff)
        .filter(Bill.reminder_sent.is_(False))
        .all()
    )


def mark_reminder_sent(bill):
    bill.reminder_sent = True
    db.session.commit()
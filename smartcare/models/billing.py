from datetime import datetime, timedelta

from smartcare.extensions import db

# Medicine bills give the patient this many days to pay before being
# flagged overdue on their dashboard and in the reminder job.
BILL_DUE_DAYS = 3


class Bill(db.Model):
    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), nullable=True)
    # Set only for medicine bills generated from a prescription — kept
    # separate from appointment_id because Appointment.bill is a strict
    # one-to-one relationship already used by the consultation-fee bill.
    prescription_id = db.Column(db.Integer, db.ForeignKey("prescriptions.id"), nullable=True)
    generated_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # "online" = patient must pay via Razorpay from their own dashboard
    # (booked their own appointment). "counter" = reception collects
    # cash/card in person (walk-in patients, or any manually-created bill).
    # This is set explicitly at creation time rather than inferred from
    # appointment_id/prescription_id, so there's exactly one source of
    # truth for which collection flow a bill belongs to.
    channel = db.Column(db.String(20), default="counter", nullable=False)

    subtotal = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    tax = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    total = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    status = db.Column(db.String(20), default="unpaid", nullable=False)  # unpaid / paid / partial / refund_pending / refunded

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Nullable so consultation-fee bills (paid instantly at booking time)
    # and counter bills (paid same-visit) don't need a due date — only
    # online medicine bills, which can sit unpaid, get one.
    due_date = db.Column(db.DateTime, nullable=True)
    # Tracks whether the "payment reminder" email has already gone out,
    # so the scheduled job never emails the same overdue bill twice.
    reminder_sent = db.Column(db.Boolean, default=False, nullable=False)

    patient = db.relationship("Patient", back_populates="bills")
    appointment = db.relationship("Appointment", back_populates="bill")
    items = db.relationship("BillItem", back_populates="bill", cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="bill", cascade="all, delete-orphan")

    @property
    def amount_paid(self):
        return sum((p.amount for p in self.payments), start=0)

    @property
    def balance_due(self):
        return self.total - self.amount_paid

    @property
    def is_overdue(self):
        if self.status == "paid" or not self.due_date:
            return False
        return datetime.utcnow() > self.due_date

    def __repr__(self):
        return f"<Bill #{self.id} total={self.total} status={self.status}>"


class BillItem(db.Model):
    __tablename__ = "bill_items"

    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"), nullable=False)

    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    line_total = db.Column(db.Numeric(10, 2), default=0, nullable=False)

    bill = db.relationship("Bill", back_populates="items")

    def __repr__(self):
        return f"<BillItem {self.description} x{self.quantity}>"


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"), nullable=False)

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(20), default="cash")  # cash / card / upi
    paid_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    bill = db.relationship("Bill", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.amount} via {self.method}>"
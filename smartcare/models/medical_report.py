from datetime import datetime

from smartcare.extensions import db


class MedicalReport(db.Model):
    __tablename__ = "medical_reports"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=True)

    title = db.Column(db.String(150), nullable=False)
    # file_path is set for uploaded scans/X-rays. results_json is set for
    # doctor-entered test values (e.g. CBC), which get rendered into a PDF
    # on demand — never stored as a static file, so there's no risk of one
    # patient's downloaded report actually containing another patient's data.
    file_path = db.Column(db.String(255), nullable=True)
    results_json = db.Column(db.Text, nullable=True)
    report_type = db.Column(db.String(30), default="lab")  # lab / scan / other
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    patient = db.relationship("Patient", back_populates="medical_reports")
    doctor = db.relationship("Doctor")

    @property
    def is_generated(self):
        """True if this report's PDF is built on-the-fly from typed-in values,
        rather than being a doctor-uploaded file."""
        return self.file_path is None and self.results_json is not None

    def __repr__(self):
        return f"<MedicalReport {self.title} patient={self.patient_id}>"
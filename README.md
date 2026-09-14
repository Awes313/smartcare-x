# 🏥 SmartCare X — Intelligent Hospital Management System

A full-featured hospital management platform built with **Python and Flask**, supporting patients, doctors, receptionists, and administrators in one connected system. The platform combines online and offline hospital workflows into a single, consistent system.

<p align="center">
  <img src="screenshots/logo.png" width="180">
</p>

**Live Demo:** https://awes77.pythonanywhere.com

**Core Skills:** Python · Flask · SQL · HTML · CSS · Bootstrap

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture Highlights](#architecture-highlights)
- [Demo Credentials](#demo-credentials)
- [Local Setup](#local-setup)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Security](#security)
- [Author](#author)

---

## 📌 Overview

SmartCare X is a hospital management system designed to handle different hospital workflows through separate role-based dashboards.

The system supports four main user roles:

- **Admin** — manages users, doctors, departments, medicines, reports, refunds, and system activity.
- **Doctor** — manages appointments, patient records, prescriptions, and availability.
- **Patient** — books appointments, makes payments, views prescriptions and medical reports, and manages appointments.
- **Receptionist** — handles walk-in patients, tokens, appointments, and counter billing.

The platform supports both **online** and **offline** hospital workflows.

### 🌐 Online Workflow

Patients can:

1. Register and log in.
2. Book an appointment.
3. Pay consultation fees online.
4. Attend video consultations when applicable.
5. Receive prescriptions.
6. Track medicine bills and payments.
7. Access their medical records and reports.

### 🏥 Offline Workflow

Receptionists can:

1. Register walk-in patients.
2. Assign appointment tokens.
3. Handle consultation billing.
4. Manage appointments at the reception desk.
5. Process counter payments.

---

## 🚀 Key Features

### 👤 Patient

- Self-registration with email verification
- Online appointment booking
- In-person and video consultation options
- Rule-based symptom-to-department suggestion
- Online consultation and medicine payments
- Appointment rescheduling and cancellation
- Digital prescriptions
- System-generated medical reports in PDF format
- Medicine bill tracking
- Automatic payment reminders
- Consolidated health timeline
- Patient reviews

### 🩺 Doctor

- Appointment approval, rejection, and completion
- Doctor availability management
- Patient record management
- Prescription creation
- Searchable medicine selection
- Dosage and frequency selection
- Automatic medicine stock deduction
- Patient-specific medical records
- Video consultation access
- Appointment state validation
- Prevention of visit completion when required payments are pending

### 🧑‍💼 Receptionist

- Walk-in patient registration
- Automatic token assignment
- Consultation fee billing
- Counter billing
- Cash, card, and UPI payment handling
- Appointment management
- Live token board
- Patient registration and lookup

### 🛡️ Admin

- Admin dashboard with analytics
- User management
- Doctor management
- Department management
- Medicine inventory management
- Appointment management
- Refund management
- Revenue and appointment reports
- CSV/PDF report exports
- Contact message management
- Audit and activity logs
- Financial record management

---

## 🛠️ Tech Stack

### Core Skills

| Technology | Usage |
|---|---|
| **Python** | Backend development, business logic, validation, automation, and application functionality |
| **Flask** | Web application framework, routing, authentication, role-based dashboards, and application structure |
| **SQL** | Managing hospital data, relationships, appointments, patients, doctors, prescriptions, billing, and inventory |
| **HTML** | Building the structure and content of web pages |
| **CSS** | Styling, layouts, spacing, responsiveness, and custom UI design |
| **Bootstrap** | Responsive layouts, navigation, forms, tables, cards, dashboards, and reusable UI components |

### Integrations

- **Razorpay** — Online payment processing for consultation and medicine bills
- **Jitsi Meet** — Video consultation functionality
- **Flask-Mail** — Email notifications and payment reminders
- **ReportLab** — PDF report generation
- **APScheduler** — Automated background tasks such as payment reminders

---

## 🗄️ Database

The application uses a relational database to store and manage structured hospital data.

SQL-based database operations are used for:

- Patient and doctor information
- User accounts and roles
- Departments
- Appointments
- Prescriptions
- Medicines and inventory
- Bills and payments
- Medical reports
- Reviews
- Notifications
- Audit and activity records

The database structure maintains relationships between different parts of the hospital system, allowing information such as appointments, prescriptions, billing, and patient records to remain connected.

---

## 🏗️ Architecture

SmartCare X follows a modular Flask application structure:

```text
app.py
   ↓
Application Factory
   ↓
Configuration
   ↓
Flask Extensions
   ↓
Blueprints
   ├── Main
   ├── Authentication
   ├── Patient
   ├── Doctor
   ├── Reception
   └── Admin
   ↓
Business Logic / Services
   ↓
Database Models
   ↓
SQL Database

---

## 🔑 Demo Credentials

| Role | Email | Password |
|---|---|---|
| Admin | `admin@smartcarex.com` | `smartcarex@7777` |
| Doctor (sample) | `drahmed@smartcarex.com` | `Doctor@123` |
| Patient (sample) | `awes51327@gmail.com` | `Rhydon7777` |

---

## ⚙️ Local Setup

```bash
# Clone the repository
git clone https://github.com/Awes313/smartcare-x.git
cd smartcare-x

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env

# Apply database migrations
flask db upgrade

# Seed demo data
flask seed-db

# Run the application
flask run

---

📁 Project Structure

smartcare-x/
├── app.py
├── config.py
├── smartcare/
│   ├── models/
│   ├── auth/
│   ├── patient/
│   ├── doctor/
│   ├── reception/
│   ├── admin/
│   ├── main/
│   ├── services/
│   ├── utils/
│   ├── emails/
│   └── templates/
├── migrations/
├── screenshots/
├── .env.example
├── .gitignore
├── LICENSE
├── requirements.txt
├── Procfile
└── README.md
```
---

# 📸 Project Screenshots

## 🏠 Home Page

The landing page showcasing SmartCare X services, featured doctors, departments, testimonials, and quick access to appointments.

<p align="center">
<img src="screenshots/home-page.png" width="900">
</p>

---

## 👨‍⚕️ Doctors Directory

Browse available doctors with specialization, consultation fees, and profile information.

<p align="center">
<img src="screenshots/doctors-directory.png" width="900">
</p>

---

## 📞 Contact Page

Patients can send inquiries or feedback directly to the hospital administration.

<p align="center">
<img src="screenshots/contact-page.png" width="900">
</p>

---

## 🛡️ Admin Dashboard

Centralized dashboard for managing users, doctors, appointments, revenue, and hospital analytics.

<p align="center">
<img src="screenshots/admin-dashboard.png" width="900">
</p>

---

## 👨‍⚕️ Manage Doctors

Add, edit, activate, or deactivate doctors while assigning departments and consultation fees.

<p align="center">
<img src="screenshots/manage-doctors.png" width="900">
</p>

---

## 👥 Manage Users

Manage patients, receptionists, and administrators with secure role-based access.

<p align="center">
<img src="screenshots/manage-users.png" width="900">
</p>

---

## 💊 Medicine Management

Maintain medicine inventory, stock levels, pricing, and availability.

<p align="center">
<img src="screenshots/medicine-management.png" width="900">
</p>

---

## 📊 Reports Dashboard

Generate and export reports related to appointments, revenue, medicines, and patients.

<p align="center">
<img src="screenshots/reports-dashboard.png" width="900">
</p>

---

## 💸 Refund Management

Manage cancelled appointment refunds and monitor payment status.

<p align="center">
<img src="screenshots/refund-management.png" width="900">
</p>

---

## 📝 Audit Logs

Track important activities performed by administrators and hospital staff.

<p align="center">
<img src="screenshots/audit-logs.png" width="900">
</p>

---

## 👨‍⚕️ Doctor Dashboard

Doctors can manage appointments, prescriptions, schedules, and patient records.

<p align="center">
<img src="screenshots/doctor-dashboard.png" width="900">
</p>

---

## 📅 Today's Appointments

Quick overview of scheduled appointments with status tracking.

<p align="center">
<img src="screenshots/today-appointments.png" width="900">
</p>

---

## 💊 Write Prescription

Doctors can create digital prescriptions with medicines, dosage, and treatment instructions.

<p align="center">
<img src="screenshots/write-prescription.png" width="900">
</p>

---

## 📋 Patient Records

Access patient medical history, prescriptions, and consultation details securely.

<p align="center">
<img src="screenshots/patient-records.png" width="900">
</p>

---

## 👤 Patient Dashboard

Patients can view appointments, prescriptions, bills, reports, and health history.

<p align="center">
<img src="screenshots/patient-dashboard.png" width="900">
</p>

---

## 📅 Appointment Booking

Book online or in-person appointments by selecting doctor, date, and consultation type.

<p align="center">
<img src="screenshots/appointment-booking.png" width="900">
</p>

---

## 📄 Prescriptions & Lab Reports

Patients can access their prescriptions and generated medical reports.

<p align="center">
<img src="screenshots/prescriptions-labreports.png" width="900">
</p>

---

## 🧑‍💼 Reception Dashboard

Receptionists can manage walk-in patients, tokens, appointments, and billing.

<p align="center">
<img src="screenshots/reception-dashboard.png" width="900">
</p>

---

## 🧾 Billing Management

Manage consultation and medicine bills with payment status tracking.

<p align="center">
<img src="screenshots/billing-management.png" width="900">
</p>

---

## 📅 Manage Appointments

Manage hospital appointments and monitor appointment status.

<p align="center">
<img src="screenshots/manage-appointments.png" width="900">
</p>

---

## 💳 Razorpay Payment

Online payment interface for consultation and medicine bills.

<p align="center">
<img src="screenshots/razorpay-payment.png" width="900">
</p>

---

## 🎥 Jitsi Video Consultation

Video consultation interface for online doctor appointments.

<p align="center">
<img src="screenshots/jitsi-video-consultation.png" width="900">
</p>

---

## 📱 Mobile Responsive View

Responsive interface optimized for different screen sizes.

<p align="center">
<img src="screenshots/mobile-responsive-view.png" width="500">
</p>

---

## ⭐ Key Highlights

- Role-based dashboards for Admin, Doctor, Patient, and Receptionist
- Online and offline hospital workflows
- Appointment booking with conflict handling
- Online payments using Razorpay
- Video consultations using Jitsi Meet
- Medicine inventory and billing management
- Digital prescriptions and medical reports
- Automated payment reminders
- PDF and CSV report generation
- Audit and activity logging
- Responsive interface using HTML, CSS, and Bootstrap

---

## 🔐 Security

- Role-based authentication and authorization
- Secure password hashing
- Email verification for user accounts
- Protected routes based on user roles
- CSRF protection for forms
- Secure payment signature verification
- Account activation and deactivation controls
- Backend validation for important operations
- Restricted access to patient medical records
- Audit logging for important system activities

---

## 👨‍💻 Author

**Mohammed Awes Tadas**

- 💻 GitHub: https://github.com/Awes313
- 🔗 LinkedIn: https://www.linkedin.com/in/awes313/
- 📧 Email: mohamed7777awes@gmail.com

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgements

- Flask documentation and community
- Bootstrap documentation
- Razorpay
- Jitsi Meet
- Python community


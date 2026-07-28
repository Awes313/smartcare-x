<p align="center">
<img src="screenshots/logo.png" width="180">
</p>

# 🏥 SmartCare X — Intelligent Hospital Management System

A production-ready Hospital Management System built with **Python, Flask, SQLAlchemy, Bootstrap 5, Razorpay, and Jitsi Meet**.

SmartCare X provides an integrated healthcare platform where **patients, doctors, receptionists, and administrators** can manage appointments, billing, prescriptions, reports, medicines, and online video consultations from one centralized system.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-blue?logo=postgresql)
![Razorpay](https://img.shields.io/badge/Razorpay-Payment-02042B?logo=razorpay)
![Jitsi](https://img.shields.io/badge/Jitsi-Video_Meeting-97979A?logo=jitsi)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌐 Live Demo

🌍 **Live Website:** https://awes77.pythonanywhere.com

---

## ✨ Key Highlights

- 👥 Role-Based Authentication (Admin, Doctor, Patient & Receptionist)
- 📅 Online & Walk-in Appointment Management
- 💳 Razorpay Payment Gateway Integration
- 🎥 Online Video Consultation using Jitsi Meet
- 💊 Medicine Inventory & Stock Management
- 📝 Digital Prescriptions
- 📄 Lab Reports
- 📈 Analytics Dashboard
- 📊 Reports Export (CSV & PDF)
- 💰 Refund Management
- 📧 Email Notifications
- 📱 Fully Responsive Design

---

# 📋 Table of Contents

- Overview
- Features
- Technology Stack
- Project Architecture
- Screenshots
- Installation
- Folder Structure
- Future Improvements
- Author

# 📖 Overview

SmartCare X is a full-stack Hospital Management System designed to simplify healthcare operations through one unified platform.

The system supports complete workflows for patients, doctors, receptionists, and administrators, allowing hospitals to efficiently manage appointments, billing, prescriptions, medicine inventory, reports, payments, and online consultations.

Unlike a basic CRUD application, SmartCare X simulates real-world hospital operations by combining online healthcare services with traditional hospital management in a single application.

---

# 🚀 Core Features

## 👤 Patient

- Register & Login securely
- Book online appointments
- Choose online or offline consultation
- Secure payment using Razorpay
- Join video consultation through Jitsi Meet
- View appointment history
- Download prescriptions
- Download lab reports
- Manage profile
- Receive email notifications

---

## 👨‍⚕️ Doctor

- Dashboard overview
- View today's appointments
- Approve or reject appointments
- Generate digital prescriptions
- Access patient medical history
- Manage availability
- Conduct online consultations
- Track completed consultations

---

## 🧑‍💼 Receptionist

- Register walk-in patients
- Create appointments
- Generate bills
- Manage patient queue
- Handle counter payments
- Manage appointment schedules

---

## 👨‍💼 Administrator

- Dashboard & Analytics
- Manage Users
- Manage Doctors
- Manage Departments
- Manage Medicines
- Generate Reports
- Refund Management
- Audit Logs
- Revenue Tracking
- System Configuration

---

# 💻 Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python, Flask, Flask-Login, Flask-WTF, Flask-Mail, Flask-Migrate |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Database** | SQLAlchemy ORM, SQLite (Development), PostgreSQL (Production Ready) |
| **Authentication** | Flask-Login, Werkzeug Password Hashing |
| **Payments** | Razorpay (Sandbox/Test Mode) |
| **Video Consultation** | Jitsi Meet |
| **Charts & Analytics** | Chart.js |
| **PDF Generation** | ReportLab |
| **Background Scheduler** | APScheduler |
| **Email Services** | SMTP (Flask-Mail) |
| **Version Control** | Git & GitHub |
| **Deployment** | PythonAnywhere |

---

# 🏗️ System Architecture

SmartCare X follows a modular Flask architecture using Blueprints and SQLAlchemy ORM. Every user role has its own dashboard, permissions, and business logic while sharing a common database and service layer.

### Main Modules

- Authentication & Authorization
- Patient Management
- Doctor Management
- Reception Management
- Appointment Management
- Billing & Payments
- Medicine Inventory
- Prescription Management
- Laboratory Reports
- Analytics Dashboard
- Refund Management
- Contact & Feedback System
- Activity Logs

---

## Workflow Overview

```text
Patient
   │
   ▼
Book Appointment
   │
   ▼
Doctor Approval
   │
   ├────────────► Online Consultation (Jitsi)
   │
   ▼
Prescription
   │
   ▼
Medicine Billing
   │
   ▼
Payment (Razorpay / Reception)
   │
   ▼
Lab Reports
   │
   ▼
Patient Dashboard
```

---

# 📁 Project Structure

```text
smartcare-x/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── migrations/
├── instance/
├── screenshots/
│
├── smartcare/
│   │
│   ├── admin/
│   ├── auth/
│   ├── doctor/
│   ├── patient/
│   ├── reception/
│   ├── main/
│   ├── models/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── forms/
│   ├── utils/
│   └── emails/
│
└── profile/
```

---

# ⚙️ Local Installation

## Clone Repository

```bash
git clone https://github.com/Awes313/smartcare-x.git

cd smartcare-x
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file and configure:

```env
SECRET_KEY=your_secret_key

MAIL_USERNAME=your_email

MAIL_PASSWORD=your_password

RAZORPAY_KEY_ID=your_key

RAZORPAY_KEY_SECRET=your_secret
```

---

## Apply Database Migration

```bash
flask db upgrade
```

---

## Seed Demo Data

```bash
flask seed-db
```

---

## Run the Project

```bash
flask run
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

# 🔑 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@smartcarex.com | smartcarex@7777 |
| **Doctor** | drahmed@smartcarex.com | SmartCare@123 |
| **Patient** | patient.aarav@smartcarex.com | SmartCare@123 |

> **Note:** These credentials are for demonstration purposes only.

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
Patients can download prescriptions and laboratory reports in PDF format.

<p align="center">
<img src="screenshots/prescriptions-labreports.png" width="900">
</p>

---

## 🧑‍💼 Reception Dashboard
Receptionists manage walk-in registrations, appointments, billing, and patient flow.

<p align="center">
<img src="screenshots/reception-dashboard.png" width="900">
</p>

---

## 💳 Billing Management
Manage consultation fees, medicine bills, and payment records efficiently.

<p align="center">
<img src="screenshots/billing-management.png" width="900">
</p>

---

## 📆 Manage Appointments
View, approve, cancel, and reschedule appointments with real-time status updates.

<p align="center">
<img src="screenshots/manage-appointments.png" width="900">
</p>

---

## 💰 Razorpay Payment Integration
Secure online payment gateway integration for appointment and medicine billing.

<p align="center">
<img src="screenshots/razorpay-payment.png" width="900">
</p>

---

## 🎥 Jitsi Video Consultation
Built-in telemedicine support using Jitsi Meet for secure online doctor consultations.

<p align="center">
<img src="screenshots/jitsi-video-consultation.png" width="900">
</p>

---

## 📱 Mobile Responsive View
Responsive user interface optimized for smartphones, tablets, and desktop devices.

<p align="center">
<img src="screenshots/mobile-responsive-view.png" width="350">
</p>

---

---

# ✨ Key Highlights

- 🏥 Complete Hospital Management Platform
- 👥 Multi-Role Authentication (Admin, Doctor, Patient & Receptionist)
- 📅 Online & Walk-in Appointment Management
- 💳 Razorpay Payment Gateway Integration
- 🎥 Jitsi Meet Video Consultation
- 💊 Smart Medicine Inventory Management
- 📄 Digital Prescriptions & Lab Reports
- 📊 Interactive Admin Analytics Dashboard
- 📧 Automated Email Notifications
- 📱 Fully Responsive Design
- 🔐 Secure Role-Based Access Control
- ⚡ Modular Flask Blueprint Architecture
- 🗂️ SQLAlchemy ORM with Migration Support
- 🚀 Production-Ready Project Structure

---

# 🔒 Security Features

- Password Hashing using Werkzeug
- Role-Based Authentication & Authorization
- CSRF Protection using Flask-WTF
- Secure Session Management
- Protected Admin Routes
- Input Validation & Form Validation
- SQLAlchemy ORM to Prevent SQL Injection
- Secure Token-Based Email Verification
- Environment Variable Configuration
- Login Required Decorators

---

# 🚀 Future Improvements

- AI Symptom Checker
- Online Pharmacy Module
- Doctor Availability Calendar
- SMS Appointment Reminders
- Insurance Claim Management
- Multi-Hospital Support
- Electronic Health Records (EHR)
- REST API for Mobile Applications
- Docker Deployment
- CI/CD Pipeline using GitHub Actions

---

# 🛠️ Built With

- Python
- Flask
- SQLAlchemy
- SQLite
- PostgreSQL
- Bootstrap 5
- JavaScript
- Chart.js
- Razorpay
- Jitsi Meet
- ReportLab
- APScheduler

---

# 📈 Project Statistics

| Feature | Status |
|---------|--------|
| Authentication System | ✅ |
| Multi-Role Dashboards | ✅ |
| Appointment Management | ✅ |
| Telemedicine | ✅ |
| Razorpay Integration | ✅ |
| Medicine Inventory | ✅ |
| Billing System | ✅ |
| Reports Generation | ✅ |
| Analytics Dashboard | ✅ |
| Responsive UI | ✅ |

---

# 🤝 Contributing

Contributions, feature suggestions, and bug reports are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# 👨‍💻 Author

## Mohammed Awes

**Python Backend Developer | Flask Developer | Full Stack Web Developer**

I'm passionate about building scalable backend applications using **Python** and **Flask**, with a strong focus on clean architecture, database design, and real-world business logic. I enjoy developing complete web applications from frontend to backend and continuously improving my software development skills.

- 🌐 **GitHub:** https://github.com/Awes313
- 💼 **LinkedIn:** https://www.linkedin.com/in/awes313/
- 📧 **Email:** mohamed7777awes@gmail.com

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 🙏 Acknowledgements

Special thanks to the open-source community and the creators of:

- Flask
- Bootstrap
- SQLAlchemy
- Razorpay
- Jitsi Meet
- Chart.js
- ReportLab

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

It motivates me to continue building more open-source projects.

---

<p align="center">
<b>⭐ Thank you for visiting SmartCare X ⭐</b>

Built with ❤️ using Python & Flask
</p>
# ClassCore - School Management System 🏫

ClassCore is a robust backend API designed to digitize school administration in Ghana. It handles student enrollment, academic grading, attendance tracking, and fee collection via Paystack.

## 🚀 Features
* **User Management:** Custom Auth for Admins, Teachers, and Students.
* **Academic Records:** Track Classes, Subjects, and Grades.
* **Attendance System:** Daily attendance marking.
* **Financial Engine:** Tuition payment recording with **Paystack Integration**.
* **REST API:** Fully documented endpoints for frontend consumption.

## 🛠 Tech Stack
* **Backend:** Python 3.12, Django 5.0
* **API:** Django REST Framework (DRF)
* **Database:** SQLite3
* **Payment Gateway:** Paystack API

## ⚙️ Setup Instructions
 Clone the repository:
   ```bash
   git clone [https://github.com/theAyiahboy/Alx_DjangoLearnLab.git]
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Method,Endpoint,Description
GET,/api/students/,List all students
POST,/api/attendance/,Mark attendance
POST,/api/payments/verify/,Verify Paystack transaction

👤 Author
Giovanni Ayiah-Mensah - ALX BACKEND DEV COHORT 7 / [https://ehub.alxafrica.com/profile/8ede5e69-1c47-4bf0-aa5f-4091b24740c0]
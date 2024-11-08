---

# Django Attendance and Announcement Management System

This Django application provides an attendance management system with user and admin functionalities. It includes features for user registration, login, OTP verification, attendance tracking, announcement management, and more.

## Features

- **User Registration & Login:** Users can register and log in using a secure system with hashed passwords.
- **OTP Verification:** Users are required to verify their identity via a One-Time Password (OTP) sent to their email.
- **Attendance Management:** Users can submit attendance, which is marked as late, absent (alpha), or on time based on the submission time.
- **Admin Dashboard:** Admin users can view all attendance records, manage user profiles, and create/edit announcements.
- **Automated Attendance:** Automatically marks absent users who haven't submitted attendance by a set time.
- **Data Export:** Admins can export attendance data to Excel format for record-keeping.
- **Announcements:** Admins can create and manage announcements visible to users.

## Requirements

- Python 3.x
- Django
- Django-MySQL-Connector
- Django-Bcrypt
- Django-APScheduler
- Pandas
- Openpyxl

## Setup

1. **Clone the Repository**

### 1. Clone the Repository

```bash
git clone https://github.com/alpiawo/Django-Attendance.git
cd <repository-directory>

2. **Install Dependencies**

   Create a virtual environment and install the required packages:

   ```bash
   python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  pip install -r requirements.txt
   ```

3. **Configure the Application**

   Update Django settings in `settings.py`:

   -Set up MySQL database connection:
     ```python
       DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'database_name',
          'USER': 'username',
          'PASSWORD': 'password',
          'HOST': 'localhost',
          'PORT': '3306',
      }
    }
     ```

   - Configure email settings for OTP:
     ```python
     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
      EMAIL_HOST = 'smtp.example.com'
      EMAIL_PORT = 587
      EMAIL_USE_TLS = True
      EMAIL_HOST_USER = 'your-email@example.com'
      EMAIL_HOST_PASSWORD = 'your-email-password'
     ```

4. **Database Setup**

   Run database migrations:

  ```python
    python manage.py migrate
  ```

   Ensure the following tables are created:

  - `user`: Stores user information.
  - `attendance`: Tracks attendance records.
  - `announcements`: Manages announcements..

## Create Superuser

```bash
  python manage.py createsuperuser
```

## Running the Application

1. **Start Django Development Server**

   ```bash
   python manage.py runserver
   ```

   The application will run at `http://localhost:8000`.

2. **Access the Application**

  - Home Page: `http://localhost:8000/`
  - Login Page: `http://localhost:8000/login`
  - Registration Page: `http://localhost:8000/register`
  - Admin Dashboard: `http://localhost:8000/admin`
  - Announcements Page: `http://localhost:8000/announcements`
  - Create Announcement: `http://localhost:8000/create-announcement`
  - Edit Announcement: `http://localhost:8000/edit-announcement/<id>`
  - Profile Page: `http://localhost:8000/profile`

## Routes

- `/:` Renders the login page.
 `/register`: Handles user registration.
- `/login`: Handles user login and OTP verification.
- `/forgot-password`: Requests a password reset.
- `/reset-password`: Resets password using OTP.
- `/verify`: Renders OTP verification page.
- `/verify-otp`: Handles OTP verification.
- `/admin`: Admin dashboard displaying user attendance data.
- `/attendance`: Handles attendance submissions.
- `/profile`: Displays and edits user profile.
- `/export-attendance`: Exports attendance data as an Excel file.
- `/announcements`: Displays all announcements.
- `/create-announcement`: Creates a new announcement.
- `/edit-announcement/<id>`: Edits an existing announcement.
- `/user/announcements`: Displays announcements for users.
- `/check_attendance`: Checks if the user has attended today.
- `/logout`: Logs out and ends the user session.

## Scheduled Tasks

- **check attendance status**: 7 days before the system checks the attendance status so that the status is not empty.
- **Mark Absences as Alpha**: Every day at 10:00 for users who haven't marked attendance.

## Notes

- Make sure to handle the secret key and database credentials securely.
- Adjust the scheduler configurations based on your application's requirements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to adjust any sections according to your specific needs or additional details you might want to include!

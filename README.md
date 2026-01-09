# DigiDoc

**Personal Healthcare Management System built using Django**

DigiDoc is a web-based healthcare management platform developed using the Django framework. It is designed to digitally manage interactions between doctors and patients, including medical records, prescriptions, reports, and user authentication.

This project was originally inspired by an academic group project and has been independently adapted, customized, and deployed as a **self project** for learning, experimentation, and portfolio demonstration.

---

## Project Structure

The software system consists of the main working directory, [`DigiDoc`](/DigiDoc), which contains the core configuration and startup code for the project, along with the following directories:

- [`doctors`](/doctors): Django application responsible for the doctor-side interface, including models, views, forms, URLs, and templates related to doctors.

- [`patients`](/patients): Django application responsible for the patient-side interface, including patient profiles, medical history access, and related functionalities.

- [`media`](/media): Stores uploaded medical documents such as prescriptions, lab reports, medical certificates, scans, and treatment files.

- [`templates`](/templates): Contains shared HTML templates and static assets used across the platform, including login, registration, home, and navigation components.

- [`db.sqlite3`](/db.sqlite3): SQLite database file used for storing application data such as users, roles, and medical records.

- [`manage.py`](/manage.py): Entry-point file used to manage and run the Django project through the command line interface.

---

## Technologies Used
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Forms & UI:** django-crispy-forms, crispy-bootstrap4

---
  Click on the following link to use the website deployed on the web: [DocuMed on PythonAnywhere](https://devanshag.pythonanywhere.com)

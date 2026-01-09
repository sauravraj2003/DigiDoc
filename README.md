# DocuMed

**Group "Ctrl C + Ctrl V"'s Repository for CS253 Course Project, IIT Kanpur.**

- This healthcare-based software system comprises of the main working directory, [`DocuMed`](/DocuMed), containing the overall code responsible for establishing the software and getting it started, and 6 other directories, which are:

  - [`Doctors`](/doctors): The directory for the Django application "doctors", for maintaining the functionalities related to the doctor side interface and all its repositories/files containing the source codes for the same. It includes the URLs, templates, models, forms, and views which constitute the entire doctor-side interface.

  - [`Patients`](/patients): Same as for Doctors above but for the patient-side interface.

  - [`Media`](/media): The folder storing all the relevant documents required for the doctors and patients' access. It includes files for prescriptions, treatments, medical certificates, lab reports, scans, etc.

  - [`Templates`](/templates): Contains the HTML templates and images which constitute the overall frontend of the project, non-specific to the doctor/patient interfaces. It includes the templates for the navbar, login, home, select profile, and registration pages, as well as background images and icons used throughout the whole software.

  - [`db.sqlite3`](/db.sqlite3): The overall database of the software which maintains the data related to all the users (patients, doctors, and admin) and the relations between them, and is responsible for querying, retrieval as well as manipulation of that data.

  - [`manage.py`](/manage.py): The file which is responsible for managing and running the entire project. It contains code for execution of the project through the command line interface and running it on the Django admin server.

- **Instructions for running the software application through the command line interface on a local server:**

  1. Firstly, type the following to get the required functionalities installed on your system:

     ```bash
     pip install django
     ```

     *Optional:* To check whether Django has been installed successfully or not, type `django-admin --version` on the command line interface. This will give you the version of Django installed on your system.

  2. After this, run the following commands step-by-step to get the additional functionalities required:

     ```bash
     pip install crispy-bootstrap4
     pip install django-crispy-forms
     ```

  3. Next, ensure that you are in the desired directory (preferably empty) of your system on the terminal.

  4. Once you have done this, run the following commands on the terminal:

     ```bash
     git clone https://github.com/devansh83/DocuMed.git
     ```

     This will clone the repository and download its contents into the required folder.

  5. Finally, to get the server up and running, navigate to the DocuMed directory (which stores the entire code, including the 6 directories) inside the folder, and enter the following on your terminal:

     ```bash
     python manage.py runserver
     ```

  6. Now you may go to your browser and type `http://localhost:8000/` to view the website.

  7. Throughout the usage of the website, ensure that the server is running on the terminal. If it closes in between, or you need to close it for some time, re-open it the next time using the command in step 5 above and after that you may view the website in the browser.

- **Instructions to operate the website deployed on the web:**

  Click on the following link to use the website deployed on the web: [DocuMed on PythonAnywhere](https://devanshag.pythonanywhere.com)

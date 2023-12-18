# TutorManager

## Project Description
**TutorManager** is a tutoring management system which aims to provide a common and convenient platform for tutors and students to keep track of lesson records and simplify lesson scheduling processes. It has five main features as follows:

**1. Tutor Search**
This feature functions as a comprehensive database of tutor profiles, where each tutor account includes details such as their name, email, years of experience, and a bio. Prospective students can utilize this database to find suitable tutors and reach out to them.

**2.	Dashboard**
The dashboard gives a clear overview of the user’s upcoming scheduled lessons.

**3.	Lesson Scheduling**
This function simplifies the process of scheduling lessons between tutors and students. Tutors can manage their available lesson slots, while students can select suitable slots based on the tutors' schedules, facilitating convenient lesson scheduling.

**4.	Lesson Records**
Tutors can create lesson records to keep track of each lesson and document students’ learning. It can also serve as a tool for tutors to leave instructions for students to prepare for upcoming lessons. The comments by the tutors can be viewed by the students.

**5.	Tutor Rating and Feedback**
Each tutor's profile includes a star rating. Students can rate tutors and recommend them to others by "starring" their profiles. Furthermore, students can post feedback on tutors' profiles to assist other students in selecting suitable tutors.


## Distinctiveness and Complexity
TutorManager is unique due to its specialized and distinctive purpose as a management system tailored to synchronize schedules and manage records for its diverse user base. Its implementation differs from other projects in several key ways:

**1. Role-based Access**

TutorManager employs a role-based access system with three main user roles: admin, tutor, and student. This role-based access is achieved through the use of Groups and permissions, which was not utilized in previous projects. Each role has distinct page displays and access to specific features:

- In Lesson Scheduling, tutors can manage their availability by adding or removing lesson slots, while students can only select available slots or cancel scheduled lessons.
- Feedback on tutors' profiles is limited to students.
- Only tutors can create lesson records, which are viewable by students.
- Admins have access to view upcoming lessons for all users.
- Role based access was implemented using Groups and permissions, which were not used in the previous projects

**2. CRUD**

TutorManager boasts a more robust set of CRUD (Create, Read, Update, Delete) functionalities compared to previous projects, offering users greater control and flexibility in managing their data. The following is a detailed list of some of the CRUD functionalities for various features.

+ Profile:
  - Users can create, view and edit their profiles.    
+ Lesson scheduling:
  - Tutors can create or remove available slots.
  -	Students can create or cancel scheduled lessons.
  -	Tutors and students can view their own upcoming scheduled lessons.
+ Lesson records:
  - Tutors can create and delete lesson records.
  - Tutors and students can view the lesson records.

## Explanation of Project Files
The project is implemented using `Django`, `Javascript`, `HTML` and `CSS`.

`tutormanager/urls.py` consists of the URL configurations for the app.

`tutormanager/models.py` defines the models that are used in the web app. Currently, there are seven models to represent the data stored in the database. 

`tutormanager/views.py` contains the views that are associated with each of the url routes.

The HTML templates can be found under the static files in `templates/tutormanager`. Each page has a separate HTML file which extends from `layout.html` and specifies the layout of the application.

Some of the HTML files also includes a Javascript file which can be found under `static/tutormanager`. The Javascript files have event listeners to the buttons in the respective pages, such that when the buttons are clicked, either there is a change in the page view or a post request is made.

The pages are mainly styled using Bootstrap, and additional custom styles are defined in `styles.css`.

## How to Run Application
1.	Download project from this github repository and unzip it.
2.	In the terminal, `cd` into the `cs50-capstone-main` directory.
3.	Run `python manage.py makemigrations tutormanager` to make migrations for the tutormanager app.
4.	Run `python manage.py migrate` to apply migrations to the database.
5.	Run `python manage.py runserver` to start the app.
6.	Register for a student/tutor account


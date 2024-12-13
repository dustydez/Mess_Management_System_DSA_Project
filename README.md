# Mess_Management_System_DSA_Project
### Project Overview
The Student Hostel Mess Management System is a streamlined application designed to efficiently manage student meal tracking and mess menus in college hostels. It aims to replace traditional mess cards with a more reliable and interactive system that offers multi-user access, data management, and validation features.

### Features
1. Student Information Management:
Track student details such as roll numbers, mess assignments, and meal consumption history.
Manage student entries during admissions or deletions at the end of an academic year.
Allow mess reassignments when required.

2. Meal History Management:
Update meal consumption records in real-time.
Prevent duplicate entries and validate meal timing restrictions.

3. Mess Menu Management:
Create, update, and delete daily menus.
Display menus interactively for specific days.

4. Multi-User Access:
Separate logins for hostel office staff and mess staff.
Mess-specific access limits data visibility to respective messes.
Advanced password management for secure logins.

5. Graphical User Interface (GUI):
User-friendly GUI built using Tkinter.
Features login pages, interactive menu displays, and student data management screens.

6. Data Validation:
Ensures only valid and authorized registration numbers are used.
Prevents redundant entries and invalid operations.

### Technical Details
Backend:
MySQL database with tables for student information, meal history, menus, and login credentials.

Frontend:
Developed in Python using Tkinter for the GUI.

Data Structures:
1. Linked Lists: Used for meal and student data.
2. Circular Doubly Linked Lists: Used for managing weekly menus.

Key SQL Tables:
1. StudentMessDetails
2. MealHistory
3. Menu
4. Login

### Setup Instructions
Database Setup:
1. Create the MySQL database and populate it with the provided schema and initial data.
2. Update the database connection details in the Python script.

Python Environment:
1. Ensure Python 3.x is installed.
2. Install required libraries: mysql.connector, tkinter.

Run the Application:
Execute the main Python script to start the application.

### Usage
Login:
Use provided credentials to access mess-specific or hostel office features.

Mess Staff:
Track student meals and update daily menus.

Hostel Office:
1. Add, update, or remove student data.
2. Handle mess reassignments.


### Contributors
Ashmita Das:
1. Database setup and interactions.
2. Login and mess management pages.
3. Password management feature.

Sahasra Pulumati:
1. Implemented data structures.
2. Designed hostel office management functionalities.

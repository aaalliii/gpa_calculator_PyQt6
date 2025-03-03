This is GPA Calculator app with PostgreSQL Data Base with GUI powered on PyQt6.

Features:

    User Registration & Login
        Stores user accounts in a PostgreSQL database.
        Option to “Remember Me” (bypass login on next launch).

    Profile Management
        Change username, profile picture (local image path), and theme preference.
        Log out functionality.

    GPA Sections
        Create multiple sections (e.g. per grade level, semester, etc.).
        Each section has a list of courses (name, grade, credits).
        Automatic GPA calculation with a simple formula ∑(grade×credits)/∑credits∑(grade×credits)/∑credits.

    Modern UI with PyQt6
        Main window shows user’s profile picture and overall GPA in the top row.
        Simple dialogs for registration, login, and editing profiles/sections.


Requirements

    Python 3.8+
    PostgreSQL (running locally or remotely)
    PyQt6
    psycopg2

Installing Dependencies
    
    pip install PyQt6 psycopg2

<img width="829" alt="изображение" src="https://github.com/user-attachments/assets/01c2b052-3949-4453-9b22-41adb9ff0a5e" />
Setting Up PostgreSQL

    Make sure PostgreSQL is installed and running.
    Create a database (e.g., gpa_db).
    Adjust connection parameters in db/db_init.py and db/db_utils.py (e.g., username, password, host, port) to match your setup.

How to Run

    Initialize the database tables. The script main.py will automatically call init_db() from db_init.py, which creates tables if they don’t already exist.
    Start the application:

          python main.py

Login or Register:

    On first run, no user is remembered, so the Login dialog will appear.
    Click “Register New User” to create an account.
    Next time you launch, if you chose “Remember Me,” the app will skip directly to the main window.


Usage Tips

    Adding Sections: In the main window, click “Add Section” to create a new GPA section.
    Double-Click a section to open its details.
    Add Courses in the section details dialog, and click “Calculate GPA”.
    Profile Picture: In the Profile dialog, click “Choose File” to select a local image. Upon saving changes, your new picture will appear in the main window’s top-left corner (rendered as a circle).
    Renaming Sections: Inside the section details dialog, edit the “Section Name” field and press “Save Section Name.”
    Delete a Section: Select the section in the main window’s list and click “Delete Selection.”

Contributing

    Fork this repo and clone to your local machine.
    Create a new branch for your feature.
    Commit your changes and push to your branch.
    Open a Pull Request for review.

Enjoy your PyQt6-based GPA Calculator! If you have any questions or issues, please open an issue or reach out.

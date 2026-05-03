📖 About This Project
This is a desktop Jukebox music app made with Python and Tkinter. 

The project has two main parts:
   **Stage 1-4:** A basic app that saves data temporarily in memory.
   **Stage 5 (Final Version):** A better app that uses **MVC design** and a **MySQL database** to save data permanently.

---

 🗂️ Project Folders

   **`Stage_1_to_4/`**: Contains the basic code, simple UI, and unit tests (Pytest).
   **`Stage_5_MVC/`**: Contains the final code. It has a modern single-window UI, connects to a database, and prevents SQL Injection.

---

## ⚙️ How to Run Stage 5 (Final Version)

Follow these steps to set up the database and run the app:

**Step 1: Install packages**
Open Terminal in the `Stage_5_MVC` folder and run:

pip install -r requirement.txt


**Step 2: Setup Database

Open XAMPP and start Apache and MySQL.

Go to http://localhost/phpmyadmin/ in your web browser.

Create a new database named exactly: oop_db

Import the oop_db.sql file (inside the Stage_5_MVC folder) into this new database.

**Step 3: Run the App
Open Terminal in the Stage_5_MVC folder and run:

Bash
python main.py
🧪 How to Run Tests (Stage 4)
To test the core logic, open Terminal in the Stage_1_to_4 folder and run:

Bash
pytest test_library_item.py -v
(All 25 test cases should pass).

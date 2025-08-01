![Screenshot_1-8-2025_111940_127 0 0 1](https://github.com/user-attachments/assets/e655b3f4-b536-4c3d-947e-3bfb3c0ea1b7)# 📅 EveSync – Smart College Event Calendar

**EveSync** is a full-stack web application built with **Flask** and **MySQL**, designed to help students, faculty, and administrators at colleges manage and track events more effectively. Inspired by everyday calendar apps, EveSync brings event scheduling and updates right to your browser — but tailored for college life.

---

## 🚀 Features

* **Role-Based Access** for Students, Faculty, and Admins
* **User Dashboard** to view college events
* **Add/Edit/Delete Events** (Faculty/Admin access)
* **Filter events by date or academic year**
* **Responsive Calendar UI**
* **Event descriptions, venue, and time display**
* **Works locally (MVP stage)**

---

## 🛠️ Tech Stack

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: Flask (Python)
* **Database**: MySQL (via XAMPP)
* **IDE**: VS Code

---

## 🧰 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/Yeshwanth-Krishna/DBMS.git
   cd DBMS
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL Database**

   * Make sure MySQL is running (e.g., via XAMPP)
   * Import the `event.sql` schema into your MySQL database
   * Update your `.env` file or configuration file with DB credentials

5. **Run the application**

   ```bash
   python app.py
   ```

---

## 🗃️ Database Schema

The app uses a single primary table:

* **event**

  * `EventID` (Primary Key, Auto-increment)
  * `EventName`
  * `EventDate`
  * `EventTime`
  * `Venue`
  * `Description`
  * *(Optional fields for image, registration link in future updates)*

---

## 📂 Project Structure

```
DBMS/
├── app.py               # Main Flask app
├── templates/           # HTML templates
├── static/              # CSS/JS/image files
├── event.sql            # Database schema
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🔍 Future Enhancements

* Online hosting & deployment
* User login system
* Event image support
* Notifications & reminders
* Registration links for events
* Admin dashboard analytics

---

## 🙏 Acknowledgements

Special thanks to:

* **Dr. Madhu B R**, Professor & Head, AIML Department
* **Dr. Soumya K N**, Assistant Professor, AIML
  for their guidance and evaluation.

---

## 💻 Demo & Source

📎 GitHub Repository:
[https://github.com/Yeshwanth-Krishna/DBMS](https://github.com/Yeshwanth-Krishna/DBMS)

---

## 📸 Project Preview
<p align="center">
  <img src="https://github.com/user-attachments/assets/bc898ce1-562d-4c22-b899-ca3baa7e07bb" width="48%" alt="EveSync UI"/>
  <img src="https://github.com/user-attachments/assets/cde17e8a-174c-45f1-b2c0-bb1cc746175d" width="48%" alt="Calendar Screenshot"/>
  <br/><br/>
  <img src="https://github.com/user-attachments/assets/5a4095a3-457a-4650-9d03-91b944c1cc3e" width="48%" alt="Screenshot 1"/>
  <img src="https://github.com/user-attachments/assets/4ee78ee9-6bc9-47a9-8403-6abcbe73febf" width="48%" alt="Screenshot 2"/>
  <br/><br/>
  <img src="https://github.com/user-attachments/assets/412b0ab9-0ff8-4ac9-9ff5-68afb6c29ca2" width="30%" alt="Screenshot 3"/>
  <img src="https://github.com/user-attachments/assets/865463e2-38ee-4da3-a618-64d2a8c879b9" width="30%" alt="Screenshot 4"/>
  <img src="https://github.com/user-attachments/assets/b0498f78-ebc1-4e9f-ad8c-1e039c216ebc" width="30%" alt="Screenshot 5"/>
  <br/><br/>
  <img src="https://github.com/user-attachments/assets/ba320b16-65e9-43fe-bb16-987c26d019e0" width="50%" alt="Final Screenshot"/>
</p>




---

## 🏷️ Tags

\#Flask #Python #MySQL #WebDevelopment
\#EventCalendar #StudentProject #EveSync
\#Teamwork #CollegeEvents #FullStackMVP


<img width="1113" height="308" alt="image" src="https://github.com/user-attachments/assets/de10a243-542d-4082-b1b5-465aab0cffde" /><img width="1113" height="308" alt="image" src="https://github.com/user-attachments/assets/e0604ca5-2422-4337-b915-51d2c2db2a88" /># 📅 EveSync – Smart College Event Calendar

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
<img width="1515" height="419" alt="1" src="https://github.com/user-attachments/assets/bc898ce1-562d-4c22-b899-ca3baa7e07bb" />
![Screenshot_1-8-2025_111734_127 0 0 1](https://github.com/user-attachments/assets/a19675a1-d8cf-4fae-a24f-a33ce4afa26b)
![Screenshot_1-8-2025_111940_127 0 0 1](https://github.com/user-attachments/assets/bb363436-5ea2-4516-8c36-8478cbc96d17)
![Screenshot_1-8-2025_11202_127 0 0 1](https://github.com/user-attachments/assets/8058b1a7-e580-4d0e-9333-b671d89dc4b2)
![123456](https://github.com/user-attachments/assets/816d3e17-205d-4e5f-acdf-a9ca59e715e3)
![12345](https://github.com/user-attachments/assets/42d664c5-813f-4c7e-9e43-2493a8f9ea02)
![1234](https://github.com/user-attachments/assets/e3bb70a5-7c48-451d-995a-1912a7e2931e)
![123](https://github.com/user-attachments/assets/77ecef55-4531-45e9-b4f1-8790bdfcf84e)
![12](https://github.com/user-attachments/assets/7aaa703d-b777-470a-835f-dbafa49be01d)


---

## 🏷️ Tags

\#Flask #Python #MySQL #WebDevelopment
\#EventCalendar #StudentProject #EveSync
\#Teamwork #CollegeEvents #FullStackMVP


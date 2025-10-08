# 🎉 Event Management System

An advanced **Event Management System** built with **Django**, **Tailwind CSS**, and **PostgreSQL**, deployed on **Render**.  
This system allows users to create, manage, and join events efficiently with role-based access control.

---

## 🚀 Features

### 👑 Admin
- Full control over the system  
- Manage **Events**, **Organizers**, and **Participants**  
- View and update all user activities  
- Delete or approve events created by organizers  

### 🧑‍💼 Organizer
- Create and manage their own events  
- Update or delete existing events  
- View and manage participants who joined their events  

### 🙋 Participant
- View all upcoming events  
- Join or register for events  
- View joined events in their dashboard  

---

## 🧰 Tech Stack

| Technology | Purpose |
|-------------|----------|
| **Django** | Backend framework for building robust and scalable web applications |
| **Tailwind CSS** | Modern utility-first CSS framework for responsive design |
| **PostgreSQL** | Relational database for storing user and event data |
| **Render** | Cloud platform for deployment and hosting |

---

## 🏗️ Project Structure

```
event_management_system/
│
├── manage.py
├── requirements.txt
├── .env
│
├── core/                # Main Django settings & configurations
├── events/              # App for event-related features
├── users/               # App for authentication & user roles
│
├── static/              # Static files (Tailwind CSS, JS)
└── media/               # Uploaded images (event banners, etc.)
```

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/event-management-system.git
cd event-management-system
```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables
Create a `.env` file in the project root and add:
```bash
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5️⃣ Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create a superuser
```bash
python manage.py createsuperuser
```

### 7️⃣ Run the development server
```bash
python manage.py runserver
```

Open your browser and visit:  
👉 **http://127.0.0.1:8000/**

---

## 🌐 Deployment (Render)

1. Push your code to a GitHub repository  
2. Create a new **Web Service** on [Render](https://render.com)  
3. Connect your repo and add environment variables under “Environment” tab  
4. Add a **PostgreSQL Database** from Render Dashboard  
5. Configure your database URL and deploy!

---

## 🧩 Role-Based Access Summary

| Role | Permissions |
|------|--------------|
| **Admin** | Manage all users and events |
| **Organizer** | Manage only their own events |
| **Participant** | View and join available events |

---


## 🛠️ Future Enhancements
- Email notifications for event updates  
- Event search and filtering  
- Chat or Q&A section for event participants  
- Integration with payment gateways for ticketed events  

---

## 🧑‍💻 Author

**Developed by:** Muhammad Shahinur  
📧 Email: shahinurislam728@gmail.com

---

## 📜 License
This project is licensed under the **MIT License** – feel free to use and modify it.

---

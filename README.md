# 🚀 Team Task Manager

A full-stack **Django-based task management system** designed to help teams organize projects, assign tasks, and track progress efficiently with **role-based access control**.

---

## 📌 Overview

This application allows organizations or small teams to:

* Manage multiple projects
* Assign tasks to users
* Track task progress and deadlines
* Identify overdue work visually
* Separate permissions between Admins and Members

---

## ✨ Key Features

### 👤 Role-Based Access

* **Admin**

  * Create projects and tasks
  * Assign tasks to users
  * View all tasks across projects
* **Member**

  * View only assigned tasks
  * Update task status

---

### 📂 Project Management

* Create and manage multiple projects
* View project-specific tasks
* Track project ownership and creation date

---

### ✅ Task Management

* Create tasks with:

  * Title
  * Description
  * Assigned user
  * Due date
  * Status
* Status types:

  * Pending
  * In Progress
  * Completed

---

### ⏰ Overdue Detection

* Tasks automatically marked as **Overdue**
* Visual highlighting for quick identification

---

### 📊 Dashboard Analytics

* Total tasks
* Tasks in progress
* Completed tasks
* Overdue tasks

---

### 🎨 UI Features

* Clean Bootstrap-based interface
* Color-coded status badges
* Responsive layout
* User-friendly navigation

---

## 🛠 Tech Stack

| Layer    | Technology      |
| -------- | --------------- |
| Backend  | Django (Python) |
| Database | SQLite (Dev)    |
| Frontend | HTML, Bootstrap |
| Styling  | Bootstrap CSS   |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/team-task-manager.git
cd team-task-manager
```

### 2️⃣ Create Virtual Environment (Recommended)

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations

```
python manage.py migrate
```

### 5️⃣ Create Superuser

```
python manage.py createsuperuser
```

### 6️⃣ Run the Server

```
python manage.py runserver
```

---

## 🔐 Demo Credentials

You can use the following credentials for testing:

**Admin**

* Username: `admin`
* Password: `admin123`

---

## 📸 Screenshots 

### Dashboard

![Dashboard](https://github.com/NivedhReddy2048/team-task-manager/blob/main/dashboard.png?raw=true)

### Project View

![Project](https://github.com/NivedhReddy2048/team-task-manager/blob/main/projectview.png?raw=true)

### Task Management

![Tasks](https://github.com/NivedhReddy2048/team-task-manager/blob/main/taskmanagement.png?raw=true)



---

## 📁 Project Structure

```
team-task-manager/
│
├── core/                # Main app (models, views, forms)
├── task_manager/        # Project settings
├── templates/           # HTML templates
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## 🔒 Security Considerations

* Role-based access control enforced
* Members restricted from unauthorized actions
* Admin-only routes protected
* Basic authentication system implemented

---

## 🚧 Future Improvements

* REST API using Django REST Framework
* JWT Authentication
* Notifications for overdue tasks
* File attachments for tasks
* Deployment with Docker/AWS

---

## 👨‍💻 Author

**Nivedh Reddy**

---

## ⭐ If you found this useful

Give it a star ⭐ on GitHub!

# TaskFlow - Project Management Application

A full-featured project management application built with Flask, PostgreSQL, and Bootstrap 5.

## Features

- **User Authentication** - Register, Login, Logout, Profile Management, Change Password
- **Dashboard** - Statistics cards showing projects, tasks, priorities, overdue items, recent activities
- **Project Management** - Create, Edit, Delete, Search, Filter projects with progress tracking
- **Multiple Team Members** - Add/remove multiple users per project with Admin/Member/Viewer roles using PostgreSQL many-to-many relationships
- **Task Management** - Create, Edit, Delete, Assign, Search, Filter tasks by status/priority
- **Workflow Board** - Drag-and-drop task management with valid transition rules
- **Activity Log** - Track all user actions (login, logout, create, update, delete)
- **Reports & Analytics** - Charts.js integration with Pie, Bar, and Line charts
- **Profile Page** - View and edit profile, change password

## Tech Stack

- **Backend:** Python 3.13, Flask
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Charts:** Chart.js
- **Architecture:** OOP, MVC, SOLID Principles

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/taskflow.git
cd taskflow
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Setup

1. Install PostgreSQL (if not already installed)
2. Open pgAdmin or psql and create the database:

```sql
CREATE DATABASE taskflow;
```

3. Run the schema file:

```bash
psql -U postgres -d taskflow -f database/schema.sql
```

### 5. Configure Environment

Edit the `.env` file with your database credentials:

```
SECRET_KEY=your_secret_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=taskflow
DB_USER=postgres
DB_PASSWORD=your_password
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

### 7. Default Login

After running the schema, a default admin user is created:

- **Email:** admin@taskflow.com
- **Password:** admin123

## Folder Structure

```
TaskFlow/
│
├── app.py                  # Flask application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── README.md               # Project documentation
│
├── models/                 # Data models (OOP)
│   ├── user.py
│   ├── project.py
│   ├── task.py
│   ├── workflow.py
│   └── activity.py
│
├── routes/                 # Flask Blueprints
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── project_routes.py
│   ├── task_routes.py
│   └── workflow_routes.py
│
├── services/               # Business logic layer
│   ├── auth_service.py
│   ├── project_service.py
│   ├── task_service.py
│   ├── workflow_service.py
│   └── report_service.py
│
├── database/               # Database layer
│   ├── db.py
│   └── schema.sql
│
├── templates/              # Jinja2 templates
│   ├── layout.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── projects.html
│   ├── project_details.html
│   ├── add_project.html
│   ├── edit_project.html
│   ├── tasks.html
│   ├── add_task.html
│   ├── edit_task.html
│   ├── workflow.html
│   ├── workflow_history.html
│   ├── reports.html
│   ├── profile.html
│   ├── profile_edit.html
│   ├── change_password.html
│   ├── 404.html
│   └── 500.html
│
├── static/                 # Static assets
│   ├── css/
│   │   ├── style.css
│   │   └── dashboard.css
│   ├── js/
│   │   ├── app.js
│   │   └── validation.js
│   └── images/
│
├── utils/                  # Utility functions
│   ├── helper.py
│   ├── validators.py
│   └── decorators.py
│
└── migrations/             # Database migrations
```

## Screenshots

*Screenshots coming soon*

## License

MIT
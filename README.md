# TaskApp — Python Flask MVC

Laravel-style MVC in Python using Flask + MySQL. Clean, minimal, no bloat.

---

## Project Structure

```
task/
├── run.py                          # Entry point (like artisan serve)
├── seed.py                         # DB seeder
├── requirements.txt
├── .env                            # Environment config
│
├── config/
│   └── config.py                   # Loads .env into Flask config
│
├── database/
│   └── schema.sql                  # Schema
│
├── app/
│   ├── __init__.py                 # App factory (create_app)
│   │
│   ├── models/                     # M — like Eloquent models
│   │   ├── base_model.py           # Shared DB helpers (all, find, delete)
│   │   ├── task_model.py           # Task queries
│   │   └── user_model.py           # User + password hashing
│   │
│   ├── controllers/                # C — like Laravel controllers
│   │   ├── auth_controller.py      # login / register / logout
│   │   └── task_controller.py      # index/create/store/show/edit/update/delete
│   │
│   ├── middleware/                  # Like Laravel middleware
│   │   └── auth_middleware.py      # @login_required, @guest_only
│   │
│   └── views/templates/            # V — like Blade templates
│       ├── layouts/base.html       # Master layout (sidebar, flash messages)
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       └── tasks/
│           ├── index.html          # Task list + stats
│           ├── create.html
│           ├── edit.html
│           └── show.html
```

---

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
Edit `.env` and set your MySQL credentials:
```
DB_HOST=localhost
DB_DATABASE=3IdeaTask
DB_USERNAME=bwr_user
DB_PASSWORD=BWR@Pass2026
SECRET_KEY=change-this-secret
```

### 3. Create the database
```bash
mysql -u root -p < database/schema.sql
```

### 4. Seed demo user
```bash
python seed.py
```

### 5. Run the app
```bash
python app.py
```

Visit: **http://localhost:7001**

Login: `tech@bwrl.in` / `Sumit@2025`

---

## Routes

| Method | URL                    | Controller Action | Description       |
|--------|------------------------|-------------------|-------------------|
| GET    | /auth/login            | auth.login        | Login page        |
| POST   | /auth/login            | auth.login        | Authenticate      |
| GET    | /auth/register         | auth.register     | Register page     |
| POST   | /auth/register         | auth.register     | Create account    |
| GET    | /auth/logout           | auth.logout       | Logout            |
| GET    | /tasks/                | task.index        | List tasks        |
| GET    | /tasks/create          | task.create       | Create form       |
| POST   | /tasks/store           | task.store        | Save new task     |
| GET    | /tasks/<id>            | task.show         | View task         |
| GET    | /tasks/<id>/edit       | task.edit         | Edit form         |
| POST   | /tasks/<id>/update     | task.update       | Save changes      |
| POST   | /tasks/<id>/delete     | task.delete       | Delete task       |

# 🎓 Student Directory System (Django)

## 🚀 Features
- View student list with pagination
- Search students by name and email
- Add new students
- Update student details
- Delete students with confirmation
- Clean UI with Bootstrap + Tailwind

## 🛠 Tech Stack
- Python
- Django (CBV)
- SQLite
- Bootstrap & Tailwind CSS

## ⚙️ Functionality
- Class-Based Views (ListView, CreateView, UpdateView, DeleteView)
- Pagination (5 records per page)
- Search with `icontains` and Q objects
- Django Messages Framework

## 📸 Screens
- Home Dashboard
- Student List
- Add / Edit Form
- Delete Confirmation

## ▶️ Run Locally
```bash
git clone <your-repo-link>
cd project-folder
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

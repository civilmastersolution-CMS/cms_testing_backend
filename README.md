# CMS Backend (Django REST Framework)

This is the backend API for **Civil Master Solution (CMS)** — a dynamic content management system where all data (products, news, projects, partners, customers, etc.) is managed by the **admin panel**.
Public users can only view the website and submit request forms to inquire about products.

---

## Features

* Django REST Framework-based backend
* PostgreSQL database integration
* CORS enabled for frontend connection
* Admin panel for managing:

  * Partnerships
  * Customerships
  * Products
  * Request Forms (user inquiries)
  * Project References
  * News
* Public API endpoints for fetching and submitting data

---

## 🛠️ Tech Stack

| Component             | Technology            |
| --------------------- | --------------------- |
| Backend Framework     | Django 5.2            |
| REST API              | Django REST Framework |
| Database              | PostgreSQL (supabase) |
| Deployment Ready      | Yes                   |
| Environment Variables | `.env` file           |
| Virtual Environment   | Python venv           |

---

## ⚙️ Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/Thantwyl/cms-backend.git
cd cms-backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate it

* **Windows**

  ```bash
  venv\Scripts\activate
  ```
* **Mac/Linux**

  ```bash
  source venv/bin/activate
  ```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup environment variables

Create a `.env` file in your project root:

```
password = eZ9udkUZPS5QqXBg

DJANGO_SECRET_KEY = 'django-insecure-dzfm4u_u9hwz07nus$&_^y%z%#8@vnv*nw%7&p5!h=mod4=$$*'
DEBUG = True
ALLOWED_HOSTS = localhost,127.0.0.1

supabase connection
DB_NAME = postgres
DB_USER = postgres
DB_PASSWORD = eZ9udkUZPS5QqXBg
DB_HOST = db.jngwmhiicwgcrcogawxi.supabase.co
DB_PORT = 5432
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

---

## 🔑 API Endpoints

| Function            | Endpoint                    | Method |
| ------------------- | --------------------------- | ------ |
| Partnerships        | `/api/partnerships/`        | GET    |
| Customerships       | `/api/customerships/`       | GET    |
| Products            | `/api/products/`            | GET    |
| Request Form        | `/api/requestforms/`        | POST   |
| Project References  | `/api/projectreferences/`   | GET    |
| News                | `/api/news/`                | GET    |
| Django Admin Panel  | `/admin/`                   | Web UI |

---

## Example Request Body

### Request Form

```json
{
    "full_name": "John Doe",
    "email_address": "John@gmail.com",
    "contact_number": "09123456789",
    "company_name": "John company",
    "country": "Japan",
    "product": null
}
```

---


##  Author

**Civil Master Solution (CMS)**
Developed by: *Thantwyl*
Repository: [GitHub - cms-backend](https://github.com/Thantwyl/cms-backend)

---

## License

This project is licensed under the **MIT License**.

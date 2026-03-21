# 🚀 SimpleMsg — Distributed Messaging System

A robust, production-oriented messaging system built with a **FastAPI backend** and a **CLI client**.
The project demonstrates modern backend architecture, security best practices, and clean separation of concerns.

---

## 📌 Overview

**SimpleMsg** is a distributed system composed of two independent layers:

* 🔹 **Backend API (FastAPI)** — handles business logic, authentication, and database operations
* 🔹 **CLI Client (Argparse)** — provides a user-friendly interface for interacting with the API

Both components communicate through a well-defined **REST API contract**.

---

## 🛠️ Tech Stack

| Layer / Role        | Technology & Version                          |
|--------------------|-----------------------------------------------|
| Language           | Python 3.13+                                  |
| Backend Framework  | FastAPI==0.110.0                              |
| ASGI Server        | Uvicorn==0.27.1                               |
| Database           | PostgreSQL                                    |
| DB Driver          | psycopg2-binary==2.9.11                       |
| JWT Implementation | python-jose[cryptography]==3.3.0              |
| Password Hashing   | bcrypt==5.0.0, passlib[bcrypt]==1.7.4         |
| CLI Client         | argparse (Standard Library)                   |
| HTTP Client        | httpx==0.27.0                                 |
| Config Management  | python-dotenv==1.2.1                          |
| Testing Framework  | pytest==8.0.0                                 |

---

## 🏗️ Architecture

The system follows a **layered architecture**:

### Backend (FastAPI)

* Uses **Pydantic models** for strict request/response validation
* Implements **JWT-based authentication (stateless)**
* Manages database communication via **psycopg2**
* Exposes REST endpoints for users and messaging

### CLI Client

* Built with **argparse**
* Communicates with API via **httpx**
* Uses a custom `@auth_required` decorator for authentication
* Stores JWT token locally in `.token` file

---

## 🛡️ Security

* 🔐 **Password Hashing** — handled using `bcrypt` (no plain-text passwords stored)
* 🎟️ **JWT Authentication** — stateless, scalable authentication system
* 🧠 **Token Persistence** — CLI stores session token locally for better UX
* 🚫 Protected routes require `Authorization: Bearer <token>`

---

## 📂 Project Structure

```
SIMPLEMSG-BACKEND/
├── app/
│   └── api/
│       ├── api_models.py
│       ├── auth.py
│       └── main.py
├── auth/
│   └── auth_user.py
├── models/
│   ├── messages.py
│   └── user.py
├── database/
│   ├── create_db.py
│   └── db_test.py
├── message_service.py
├── user_service.py
├── .env
├── requirements.txt
└── README.md
```

---

## 📦 Layer Breakdown

### 📂 `app/api/` — Interface Layer

Handles HTTP communication, validation, and security.

* **api_models.py**
  Defines Pydantic schemas for validation (User, Message, Token)

* **auth.py**
  Core security module:

  * JWT generation & validation
  * Password verification (bcrypt)
  * Database dependency (`get_db`)
  * `get_current_user` for protected routes

* **main.py**
  Entry point:

  * Defines API routes
  * Connects service layer with API
  * Handles dependency injection

---

### 📂 `auth/` — CLI Authentication

* **auth_user.py**

  * Stores JWT token in `.token`
  * Implements `@auth_required` decorator
  * Handles login via API (`/auth/token`)
  * Automatically injects token into requests

💡 The `.token` file is generated automatically after successful login.

---

### 📂 `models/` — Data Access Layer (DAL)

Uses **raw SQL + psycopg2** with an **Active Record pattern**.

* **user.py**

  * Handles CRUD operations
  * Password hashing (bcrypt)
  * Context manager for DB connections
  * Secure password updates

* **messages.py**

  * Message persistence
  * User-to-user relationships
  * Message history retrieval

---

### 📂 `database/` — Database Management

* **create_db.py**

  * Creates database and tables
  * Defines schema (users, messages)
  * Ensures idempotency

* **db_test.py**

  * Integration tests using pytest
  * Validates DB connection and data integrity

---

### 📂 CLI Layer

* **user_service.py**

  * User registration, login, deletion
  * Profile management
  * Uses centralized httpx client

* **message_service.py**

  * Send messages
  * Retrieve inbox
  * Protected by authentication decorator

---

## ⚡ Key Features

* 🧩 Distributed architecture (API + CLI)
* 🔐 Secure authentication (JWT + bcrypt)
* 🧠 Clean separation of concerns
* 📦 Active Record pattern
* ⚡ FastAPI performance & validation
* 🗄️ Full control over SQL (no ORM)
* 🧪 Database integration testing
* 💻 Developer-friendly CLI interface

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/your-username/simplemsg.git
cd simplemsg
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment

Create `.env` file:

```
USER = "db_user"
HOST = "localhost"
PASSWORD = "db_password"
DATABASE = "db_name"

SECRET_KEY = "secret"
ALGORITHM = "HS256"
```

---

### 5. Initialize database

```bash
python database/create_db.py
```

---

### 6. Run FastAPI server

```bash
uvicorn app.api.main:app --reload
```

---

## 🚀 Usage (CLI)

### Register user

```bash
python user_service.py -u testuser -p password123 -fn Jan -ln Kowalski
```

### Login

```bash
python user_service.py -lo -u testuser -p password123
```

### List all registered users

```bash
python user_service.py -l
```
### Change password (Requires providing the current password and the new one)

```bash
python user_service.py -e -p old_password123 -n new_password_secure
```
### Delete account

```bash
python user_service.py -d
```

### Send message

```bash
python message_service.py -s -t 1 -tx "Hello!"
```

### Get messages

```bash
python message_service.py -l
```

---

## 🧪 Testing

```bash
pytest database/db_test.py
```

---

## 🧠 Design Decisions

* **Active Record Pattern** — simplifies service layer
* **Raw SQL** — full control over queries and performance
* **JWT (Stateless Auth)** — scalable and memory-efficient
* **Decorator-based CLI security** — clean and reusable authentication logic

---

## 📈 Future Improvements

* Docker support 🐳
* CI/CD pipeline
* Web frontend (React) or js
* Message notifications (WebSockets)
* Role-based access control

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📜 License

This project is licensed under the MIT License.

---

## 💬 Final Note

This project is not just a simple script — it demonstrates real-world backend engineering practices including **security, architecture, and scalability**.

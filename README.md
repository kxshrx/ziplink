# ziplink

## TL;DR

- **Setup:**
  ```sh
  python3 -m venv urlvenv
  source urlvenv/bin/activate
  pip install -r requirements.txt
  openssl rand -hex 32  # For SECRET_KEY
  ```
- **.env variables to set:**
  - `SECRET_KEY` (required, use the command above)
  - `ALGORITHM` (default: HS256)
- **Run:**
  ```sh
  uvicorn main:app --reload --port 8000
  ```
- **App runs on:** http://localhost:8000
- **API docs:** http://localhost:8000/docs

---

## Overview

A professional, minimal FastAPI-based URL shortener with user authentication, JWT security, per-user URL management, and full admin endpoints.

---

## Features

- User registration and login (JWT-based authentication)
- Passwords securely hashed (bcrypt)
- Authenticated users can:
  - Shorten URLs (unique per user)
  - View all their shortened URLs
  - Redirect via short code
  - View and update their profile/password
- Access count tracked for each short URL
- **Admin endpoints:**
  - List/delete any URL
  - List/delete any user (and their URLs)
  - All admin endpoints require the user to have `role='admin'`

---

## Project Structure

- `main.py` – FastAPI entry point, includes all routers
- `database.py` – SQLAlchemy setup for SQLite
- `models.py` – User and URL models
- `routers/` – API endpoints:
  - `auth.py` – Registration, login, JWT, password hashing
  - `users.py` – Profile and password management
  - `urls.py` – URL shortening, redirection, listing
  - `admin.py` – Admin endpoints for user and URL management

---

## Setup

1. **Clone and set up a virtual environment:**
   ```sh
   python3 -m venv urlvenv
   source urlvenv/bin/activate
   pip install -r requirements.txt
   ```
2. **Set up environment variables:**
   - Create a `.env` file in the project root.
   - Generate a secure secret key:
     ```sh
     openssl rand -hex 32
     ```
   - Example `.env`:
     ```
     SECRET_KEY=your_generated_key
     ALGORITHM=HS256
     ```
   - **Update these variables as needed for your deployment.**
3. **Run the app:**
   ```sh
   uvicorn main:app --reload --port 8000
   ```
   - The app will be available at http://localhost:8000
   - API docs at http://localhost:8000/docs

---

## API Endpoints

### Auth

- `POST /auth/` – Register a new user
- `POST /auth/token` – Login and get JWT token

### Users

- `GET /users/` – Get current user profile (JWT required)
- `PUT /users/password` – Update password (JWT required)

### URLs

- `POST /urls/` – Shorten a new URL (JWT required)
- `GET /urls/` – List all your shortened URLs (JWT required)
- `GET /urls/{short_code}` – Redirect to the original URL (public)

### Admin (admin role required)

- `GET /admin/urls` – List all URLs
- `DELETE /admin/urls/{short_code}` – Delete a URL by short code
- `GET /admin/users` – List all users
- `DELETE /admin/users/{userid}` – Delete a user and all their URLs

---

## How it Works

- **Registration/Login:**
  - Register with email, username, password, and role
  - Login returns a JWT token for authentication
- **Shorten URLs:**
  - Authenticated users can shorten URLs; each gets a unique short code
  - Duplicate long URLs for the same user return the existing short code
- **Redirection:**
  - Anyone can use `/urls/{short_code}` to be redirected
  - Access count is incremented on each redirect
- **User Management:**
  - Authenticated users can view/update their profile and password
- **Admin:**
  - Admins can list/delete any user or URL via `/admin` endpoints
  - All admin endpoints require the user to have `role='admin'`

---

## Tips

- Use `openssl rand -hex 32` to generate a strong secret key for your `.env`
- The SQLite database (`url.db`) and environment files are gitignored for safety

---

## License

MIT

https://roadmap.sh/projects/url-shortening-service

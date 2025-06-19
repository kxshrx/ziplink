# URL Shortener

A minimal FastAPI-based URL shortener with user authentication and management.

## Quick Start

1. **Clone the repo and set up a virtual environment:**
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

3. **Run the app:**
   ```sh
   uvicorn main:app --reload
   ```

## Project Structure

- `main.py` – FastAPI entry point, includes routers for URLs, users, and auth.
- `database.py` – SQLAlchemy setup for SQLite.
- `models.py` – User and URL models.
- `routers/` – API endpoints:
  - `auth.py` – User registration, login, JWT authentication.
  - `users.py` – User profile and password management.
  - `urls.py` – Create, fetch, and redirect short URLs.

## Workflow Overview

- **Auth:**  
  Users register and log in. JWT tokens are used for authentication. Passwords are securely hashed.

- **Users:**  
  Authenticated users can view their profile and update their password.

- **URLs:**  
  Authenticated users can shorten URLs. Each short URL is unique and tracks access count. Redirection is handled via the short code.

## Tips

- Use `openssl rand -hex 32` to generate a strong secret key for your `.env`.
- The SQLite database (`url.db`) and environment files are gitignored for safety.

## License

MIT

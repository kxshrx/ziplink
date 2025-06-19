# URL Shortener

A simple URL shortener service built with FastAPI and SQLite.

## Features
- Shorten long URLs
- Redirect to original URLs
- Admin and user management

## Project Structure
- `main.py`: FastAPI app entry point
- `database.py`: Database setup and connection
- `models.py`: SQLAlchemy models
- `routers/`: API route modules (admin, urls, users)

## Setup
1. Create and activate a virtual environment:
   ```sh
   python3 -m venv urlvenv
   source urlvenv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install fastapi uvicorn sqlalchemy python-dotenv
   ```
3. Run the application:
   ```sh
   uvicorn main:app --reload
   ```

## Notes
- The SQLite database file (`url.db`) is ignored by git.
- Environment variables can be set in a `.env` file (also gitignored).

## License
MIT

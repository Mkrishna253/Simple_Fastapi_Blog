# FastAPI Blog

Simple full-stack blog app built with FastAPI, async SQLAlchemy, SQLite, and Jinja2 templates.

## Features

- JWT auth (register, login, current user)
- Create, update, delete posts
- User profile update + profile picture upload
- Forgot/reset password flow (email)
- Server-rendered pages + JSON API
- Pagination support for posts

## Tech Stack

- FastAPI
- SQLAlchemy 2.0 (async)
- SQLite (aiosqlite)
- Alembic migrations
- Pydantic / pydantic-settings
- Jinja2 templates
- PyJWT + pwdlib
- Pillow (image processing)

## Project Structure

```text
my_fastapi_blog/
|-- main.py
|-- auth.py
|-- config.py
|-- database.py
|-- models.py
|-- schemas.py
|-- routers/
|   |-- users.py
|   `-- posts.py
|-- templates/
|-- static/
|-- media/
`-- alembic/
```

## Setup

1. Create and activate virtual env:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a .env file in the project root with your credentials:


4. Run migrations:

```bash
alembic upgrade head
```

5. Start app:

```bash
fastapi dev main.py
```

Open http://127.0.0.1:8000 and use http://127.0.0.1:8000/docs for API docs.

## Optional: Seed Demo Data

```bash
python populate_db.py
```

This clears existing users/posts/reset tokens/profile images and loads sample users, posts, and profile pictures.

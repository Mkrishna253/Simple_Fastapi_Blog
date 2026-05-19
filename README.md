# FastAPI Blog

A simple blog project built with FastAPI, SQLAlchemy, SQLite, and Jinja2 templates.

## Features

- Create, read, update, and delete users
- Create, read, update, and delete posts
- Server-rendered pages for home, post detail, and user posts
- Static and media file serving
- SQLite database for local development

## Tech Stack

- FastAPI
- SQLAlchemy (ORM)
- Pydantic
- Jinja2 Templates
- SQLite
- Uvicorn

## Project Structure

```text
my_fastapi_blog/
|-- main.py
|-- models.py
|-- schema.py
|-- database.py
|-- blog.db
|-- templates/
|   |-- layout.html
|   |-- home.html
|   |-- post.html
|   |-- user_posts.html
|   `-- error.html
|-- static/
|   |-- css/
|   |   `-- main.css
|   |-- js/
|   |   `-- utils.js
|   |-- icons/
|   `-- site.webmanifest
`-- media/
    `-- profile_pics/
```

## Setup and Run

1. Clone the repository:

```bash
git clone <your-repo-url>
cd my_fastapi_blog
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy jinja2 pydantic email-validator
```

4. Run the app:

```bash
uvicorn main:app --reload
```

5. Open in browser:

- Home page: http://127.0.0.1:8000/
- API docs (Swagger UI): http://127.0.0.1:8000/docs

## Main API Endpoints

### Users

- POST /api/users
- GET /api/users/{user_id}
- PATCH /api/users/{user_id}
- DELETE /api/users/{user_id}
- GET /api/users/{user_id}/posts

### Posts

- GET /api/posts
- POST /api/posts
- GET /api/posts/{post_id}
- PUT /api/posts/{post_id}
- PATCH /api/posts/{post_id}
- DELETE /api/posts/{post_id}

## Notes

- Database tables are created automatically at startup.
- The SQLite database file is `blog.db` in the project root.
- Static files are served from `/static` and uploaded media from `/media`.

## Credits

- Corey Schafer (@coreymschafer) for tutorial inspiration.

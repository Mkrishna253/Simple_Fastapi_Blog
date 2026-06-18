# FastAPI Blog

A full-stack blog app I built with FastAPI, async SQLAlchemy, SQLite, and Jinja2. It's got both server-rendered pages and a JSON API—no frontend framework needed, just HTML, CSS, and vanilla JS.

The app lets you register, log in, create and edit posts, upload profile pictures, reset your password, and all that fun stuff. It's basically a working blog in a box.

## What's in It

- User auth with JWT tokens (the OAuth2 way)
- Sign up and log in
- Create, edit, delete your own posts
- Update your profile and profile picture
- Actually working password reset (with email)
- Pagination that doesn't suck (offset/limit with "Load More" buttons)
- Custom error pages that don't look like garbage
- Async everything because blocking is for sync code

## Stack

FastAPI (obviously), async SQLAlchemy 2.0, SQLite with aiosqlite, Pydantic for validation, Jinja2 for templates, PyJWT, pwdlib for hashing passwords, Pillow for image processing, and aiosmtplib to send emails. Pretty standard modern Python stack.

## Project Structure

```text
my_fastapi_blog/
|-- main.py
|-- auth.py
|-- config.py
|-- database.py
|-- models.py
|-- schemas.py
|-- email_utils.py
|-- image_utils.py
|-- populate_db.py
|-- test_smtp.py
|-- blog.db
|-- routers/
|   |-- users.py
|   `-- posts.py
|-- templates/
|   |-- layout.html
|   |-- home.html
|   |-- post.html
|   |-- user_posts.html
|   |-- login.html
|   |-- register.html
|   |-- account.html
|   |-- error.html
|   `-- email/
|       `-- password_reset.html
|-- static/
|   |-- css/
|   |   `-- main.css
|   |-- js/
|   |   |-- auth.js
|   |   `-- utils.js
|   |-- icons/
|   |-- profile_pics/
|   `-- site.webmanifest
|-- media/
|   `-- profile_pics/
`-- populate_images/
```

## Getting It Running

**Clone the repo:**
```bash
git clone <your-repo-url>
cd my_fastapi_blog
```

**Set up a virtual environment (Windows):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Install everything:**
```bash
pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite pydantic pydantic-settings email-validator jinja2 pyjwt pwdlib python-multipart pillow aiosmtplib httpx
```

**Create a `.env` file** in the project root with this stuff:
```env
SECRET_KEY=replace-with-something-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

MAX_UPLOAD_SIZE_BYTES=5242880
POSTS_PER_PAGE=10
RESET_TOKEN_EXPIRE_MINUTES=60

MAIL_SERVER=localhost
MAIL_PORT=2525
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=noreply@example.com
MAIL_USE_TLS=true

FRONTEND_URL=http://localhost:8000
```

**Start the dev server:**
```bash
fastapi dev main.py
```

or if you prefer uvicorn:
```bash
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/ and poke around. API docs are at `/docs`.

## Seed Some Demo Data

If you want to actually see the blog with content instead of staring at empty tables:

```bash
python populate_db.py
```

This script will:
- Wipe everything (users, posts, tokens, profile pics—you've been warned)
- Create 6 sample users with passwords like `TestPassword1!`
- Upload profile images for most of them
- Create 45 sample blog posts with backdated timestamps so you can test pagination without going insane

The posts are all real (well, actual nonsense I wrote), so you'll actually have something to scroll through.

## How It Works (User Perspective)

1. You hit `/register`, fill out the form, and create an account
2. Log in at `/login` with your email and password
3. You get a JWT token that the JS stores in localStorage
4. Now you can create posts, edit them, delete them, whatever
5. Click on `/account` to update your profile or upload a profile picture
6. If you forget your password, there's a reset flow that emails you a token link
7. Delete your account if you hate it, and all your posts go with you

The whole thing is pretty straightforward—nothing fancy.

## API Endpoints

Honestly, the endpoints are pretty self-explanatory if you know REST. Check `/docs` for the full interactive Swagger UI, but here's the rundown:

**Auth stuff:**
- `POST /api/users` — register
- `POST /api/users/token` — login (yes, the OAuth2 form field calls it "username" but we use email)
- `GET /api/users/me` — who am I?
- `POST /api/users/forgot-password` — I forgot my password, send me a reset link
- `POST /api/users/reset-password` — here's my reset token and new password
- `PATCH /api/users/me/password` — change password while logged in

**User stuff:**
- `GET /api/users/{user_id}` — get someone's public profile
- `GET /api/users/{user_id}/posts?skip=0&limit=10` — their posts
- `PATCH /api/users/{user_id}` — update your own profile (username, email)
- `DELETE /api/users/{user_id}` — nuke your account
- `PATCH /api/users/{user_id}/picture` — upload a profile picture
- `DELETE /api/users/{user_id}/picture` — remove profile picture

**Post stuff:**
- `GET /api/posts?skip=0&limit=10` — list all posts
- `POST /api/posts` — write a post (need auth)
- `GET /api/posts/{post_id}` — read one post
- `PUT /api/posts/{post_id}` — replace entire post (your post only)
- `PATCH /api/posts/{post_id}` — edit specific fields (your post only)
- `DELETE /api/posts/{post_id}` — delete it

## Random Stuff You Should Know

- Database tables are created automatically when you start the app (that's the `lifespan` context manager doing its thing)
- The DB is just `blog.db` in the root—SQLite is fine for this
- Static files live in `/static`, user uploads in `/media`
- Profile pictures get squished down to 300x300 JPEG to keep file sizes reasonable
- The account page has a placeholder for password change UI, but the actual API endpoint works fine
- If you want to test the password reset email flow, set up MailTrap or similar in your `.env`
- The "Load More" button on the home and user pages is client-side pagination with vanilla JS—no framework nonsense

## Credits

This is based on Corey Schafer's tutorial style but built with async SQLAlchemy 2.0, modern FastAPI patterns, and all the stuff you'd actually need in a real project (password reset, image uploads, pagination that doesn't suck, etc.).

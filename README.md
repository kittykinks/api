# KittyKinks API

FastAPI backend for the KittyKinks "link in bio" experience. It handles Discord OAuth login,
site profiles, kink catalog and ratings, plus link management for user sites.

## Features

- Discord OAuth login with session cookies.
- User profile sites with avatar/banner and link lists.
- Kink catalog with per-user ratings/comments.
- Tortoise ORM models and Aerich migrations.

## Project layout

```
kittyk/
  __init__.py        # FastAPI app entrypoint + middleware + router setup
  api/               # Route handlers, schemas, errors, and dependencies
  db/                # Tortoise ORM config + models + migrations
  lib/               # Integrations (Discord, Catbox) + settings loader
```

## Requirements

- Python 3.13+
- A database (SQLite by default, PostgreSQL recommended for production)

## Configuration

The app uses environment variables loaded via `python-dotenv`:

- `DISCORD_CLIENT_ID`
- `DISCORD_CLIENT_SECRET`
- `DISCORD_REDIRECT_URI`
- `DATABASE_URL` (defaults to `sqlite://:memory:`)
- `LOGIN_NEXT_URL` (defaults to `/`)

## Quick start

1. Install dependencies (uses `uv` for dependency management):

   ```bash
   uv sync
   ```

2. Run the API:

   ```bash
   fastapi run kittyk
   ```

3. Open API docs at `http://localhost:8000/docs`.

## Database & migrations

Migrations are managed by Aerich. On app startup, the API runs migrations and initializes the
database connection. If the `kinks` table is empty, it seeds from `kinks.json`.

To run PostgreSQL locally, use the provided compose file:

```bash
docker compose up -d
```

Then set `DATABASE_URL` to a Postgres connection string (example):

```
DATABASE_URL=postgres://kittyk:kittyk@localhost:5432/kittyk
```

## Development notes

- The API authenticates requests via the `session` cookie produced by Discord login.
- CORS is configured to allow `https://kittyk.xyz` and `http://localhost:3000`.


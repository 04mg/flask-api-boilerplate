# Flask API Template

This is a template for a Flask API. It uses Flask-SQLAlchemy and Flask-Migrate extensions for data persistence and migrations.

# Setup

Init the database and run migrations:

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

Run Flask:

```bash
flask run
```

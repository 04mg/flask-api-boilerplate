# Flask API Template

This is a template for a Flask API. It relies on the following extensions:

- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate

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

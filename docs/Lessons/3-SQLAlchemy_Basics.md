### Hello App with Flask-SQLAlchemy part

Install:

```
pip3 install flask, flask-sqlalchemy, sqlalchemy
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

dburi = "postgresql://postgres:postgres@localhost:5432/postgres"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dburi

@app.route("/")
def index():
    person = Person.query.first()
    name = person.name if person else "World"
    return f"hello {name}!"

db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)
```


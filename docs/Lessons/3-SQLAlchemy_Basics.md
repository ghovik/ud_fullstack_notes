![img](https://video.udacity-data.com/topher/2019/August/5d5a4854_sqlalchemy-layers/sqlalchemy-layers.png)

![img](https://video.udacity-data.com/topher/2019/August/5d5a48b0_screen-shot-2019-08-18-at-11.58.46-pm/screen-shot-2019-08-18-at-11.58.46-pm.png)



![img](https://video.udacity-data.com/topher/2019/August/5d5a48fb_screen-shot-2019-08-18-at-11.59.53-pm/screen-shot-2019-08-18-at-11.59.53-pm.png)



![img](https://video.udacity-data.com/topher/2019/August/5d5a4906_screen-shot-2019-08-19-at-12.00.00-am/screen-shot-2019-08-19-at-12.00.00-am.png)



### Hello App with Flask-SQLAlchemy

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

    # add a wrapper that is easy for debugging
    # so every time we query this time, the result will be
    # printed automatically
    def __repr__(self):
        return f"<Person {self.id}, name: {self.name}>"

db.create_all() # create all defined tables if not exist


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)
```



#### Use a Python prompt to interact with Postgres

```shell
# Query
>>> from flask_hello_app import Person
>>> rec = Person.query.first()
>>> print(rec)
rec = Person.query.first()

# Insert
>>> from flask_hello_app import db
>>> session = db.session()
>>> john = Person(name="John")
>>> session.add(john)
>>> session.commit()
>>> session.close()
```



### SQLAlchemy Data Types

- [Flask-SQLAlchemy: Declaring Models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/)
- [Getting Started with PostgreSQL Data Types](http://www.postgresqltutorial.com/postgresql-data-types/)



### SQLAlchemy Constraints

#### Implementing a check constraint

```python
class Product(db.Model):
  ...
  price = db.Column(db.Float, db.CheckConstraint('price>0'))
```

This ensures that no `product` goes into the table with a nonpositive price value.
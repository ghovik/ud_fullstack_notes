## 3 - SQLAlchemy Basics

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



## 4 - SQLAlchemy ORM in Depth

### Introduction

<iframe width="653" height="367" src="https://www.youtube.com/embed/tLhPw16OamI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<iframe width="770" height="433" src="https://www.youtube.com/embed/MQCeKfH8KaM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



### Model.query

<iframe width="770" height="433" src="https://www.youtube.com/embed/Y7BcAESBGmM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Filtering

```python
Person.query.filter_by(name="Amy")
Person.query.all()
Person.query.count()
Person.query.filter(Person.name == "Amy")
Person.query.filter(Person.name == "Amy", Team.name == "Udacity")
Person.query.get(1) # gets by pk

# a bulk deletion example
Product.query.filter_by(category="Misc").delete()

# Query chaining examples
Person.query
	.filter(Person.name == "Amy")
    .filter(Team.name == "Udacity")
    .first()
# which is equivalent to following
db.seesion.query(Person)
	.filter(Person.name == "Amy")
    .filter(Team.name == "Udacity")
    .first()
    
Driver.query
	.join("vehicles")
    .filter_by(driver_id=3)
    .all()
    
# like statement
Person.query.filter(Person.name.like("A%"))
# [<Person 2, name: Amy>, <Person 4, name: Anne>]
```

More filtering methods can be found at [common filter operators here](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#common-filter-operators).

#### Ordering

##### order_by

```python
MyModel.order_by(MyModel.created_at) # ascending
MyModel.order_by(db.desc(MyModel.created_at)) # descending
```

##### limit

```python
Order.query.limit(100).all()
```

#### Aggregates

```python
query = Task.query.filter(complted=True)
query.count() # return number of records
```



[Click here](https://video.udacity-data.com/topher/2019/August/5d5a52af_query-cheat-sheet/query-cheat-sheet.pdf) to access a **cheat sheet** of handy SQLAlchemy Query methods to use.

Handy resources：[Docs for the SQLAlchemy Query API](https://docs.sqlalchemy.org/en/latest/orm/query.html)



### SQLAlchemy Object Lifecycle

<iframe width="770" height="433" src="https://www.youtube.com/embed/1zMqtV3Kv-0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Flush

A flush takes pending changes and translates them into SQL commands, ready to be committed to the database.



<iframe width="770" height="433" src="https://www.youtube.com/embed/GGGWgRLC80s" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

- A **flush** takes pending changes, and translates them into commands *ready* to be committed. It occurs:
- when you call `Query`. Or
- on `db.session.commit()`



## 5 - Build a CRUD App with SQLAlchemy Part 1

### Introduction

<iframe width="770" height="433" src="https://www.youtube.com/embed/EKbYqJTP0CA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<iframe width="770" height="433" src="https://www.youtube.com/embed/MZ-4WZT_Qno" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Create a Dummy ToDo App

<iframe width="770" height="433" src="https://www.youtube.com/embed/wM4cUqAM-PE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

By default, Flask looks for all your templates in a folder "templates" in your project dir.



Jinja2 is able to convert non-html data to html files. Example:

```python
from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "index.html", 
        # data can be used in html file.
        data=[{"description": f"Todo {i}"} for i in range(1, 4)])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)
```

```html
<html>
    <head>
        <title>ToDo App</title>
    </head>
    <body>
        <ul>
            <!-- data from python code -->
            {% for d in data %}
            <li>{{ d.description }}</li>
            {% endfor %}
        </ul>
    </body>
</html>
```


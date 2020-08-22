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



### "R" in CRUD

<iframe width="770" height="433" src="https://www.youtube.com/embed/FhSxO_NuvBk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Instead of fetching some mock data, now we read data from our database.

1. We need a model that stores our todos, with id as the pk and descriptions.
2. Insert some data into the model `todos`.
3. the `data` in `index()` is now read from `todos`.

```python
from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

uri = "postgresql://postgres:postgres@localhost:5432/postgres"
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = uri

class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Todo {self.id} {self.description}>"

db.create_all()

@app.route("/")
def index():
    return render_template(
        "index.html", 
        data=Todo.query.all())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)

```



### MVC - Model View Controller

<iframe width="770" height="433" src="https://www.youtube.com/embed/Dzvu8fj3ymo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Models and Views don't talk to each other directly, they do so through Controllers.



![MVC](https://video.udacity-data.com/topher/2019/August/5d5dc48f_screen-shot-2019-08-21-at-3.23.56-pm/screen-shot-2019-08-21-at-3.23.56-pm.png)

### Handling User Input

1. **How we accept and get user data** in the context of a Flask app
2. **Send data in controllers** using database sessions in a controller
3. **Manipulating models** adding records in SQLAlchemy Models
4. **Direct how the view should update** within the controller and views



### Getting User Data in Flask

<iframe width="770" height="433" src="https://www.youtube.com/embed/jq_mXDRzs5o" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### URL query parameters

- URL query parameters are listed as key-value pairs at the end of a URL, preceding a "?" question mark. E.g. `www.example.com/hello?my_key=my_value`.

#### Form data

- `request.form.get('<name>')` reads the `value` from a form input control (text input, number input, password input, etc) by the `name` attribute on the input HTML element.

#### Note: defaults

- `request.args.get`, `request.form.get` both accept an optional second parameter, e.g. `request.args.get('foo', 'my default')`, set to a default value, in case the result is empty.

#### JSON

- `request.data` retrieves JSON *as a string*. Then we'd take that string and turn it into python constructs by calling `json.loads` on the `request.data` string to turn it into lists and dictionaries in Python.



![img](https://video.udacity-data.com/topher/2019/August/5d5dcb03_screen-shot-2019-08-21-at-3.51.37-pm/screen-shot-2019-08-21-at-3.51.37-pm.png)

<iframe width="770" height="433" src="https://www.youtube.com/embed/fn_M1nXU0bI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<iframe width="770" height="433" src="https://www.youtube.com/embed/o_uprLVX67M" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Video Correction Notes

- "Response Body" should be corrected to "Request Body", throughout, since the client is sending off a *request*.

<iframe width="770" height="433" src="https://www.youtube.com/embed/PO-ILweiQwU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Video Correction Notes

- Response Body should be changed to Request Body, throughout.

<iframe width="770" height="433" src="https://www.youtube.com/embed/Idxfh3svV0E" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Developing the controller

<iframe width="770" height="433" src="https://www.youtube.com/embed/fRvfHuVUI4w" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

```python
from flask import request, redirect, url_for

@app.route("/todo/create", methods=["POST"])
def create():
    todo = request.form.get("todo", "")
    rec = Todo(description=todo)
    db.session.add(rec)
    db.session.commit()
    db.session.close()
    return redirect(url_for("index"))
    # here index is the name of the function index()
```

Add a form in index.html:

```html
<form method="post" action="/todo/create">
            <label for="todo">todo:</label>
            <input type="text" name="todo">
            <input type="submit", value="submit">
        </form>
```

### Using AJAX to send data to flask asynchronously

<iframe width="770" height="433" src="https://www.youtube.com/embed/sgkzOCjg7uE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

**Async data requests** - sent to the server and back to the client **without a page refresh**.

#### Using `XMLHttpRequest`

<iframe width="770" height="433" src="https://www.youtube.com/embed/-1AKXIkYwMw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Using `fetch`

<iframe width="770" height="433" src="https://www.youtube.com/embed/vR5sn_XQ17Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

```
fetch('/my/request', {
  method: 'POST',
  body: JSON.stringify({
    'description': 'some description here'
  }),
  headers: {
    'Content-Type': 'application/json'
  }
});
```

<iframe width="770" height="433" src="https://www.youtube.com/embed/qrmmZTQHDgA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Using sessions in controllers

<iframe width="770" height="433" src="https://www.youtube.com/embed/kGOfBQiQ5wE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Pattern (try-except-finally)

```python
 import sys

 try:
   todo = Todo(description=description)
   db.session.add(todo)
   db.session.commit()
 except:
   db.session.rollback()
   error=True
   print(sys.exc_info())
 finally:
   db.session.close()
```

<iframe width="770" height="433" src="https://www.youtube.com/embed/1inRXocQn_I" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Video Correction Notes

The route handler should always return something or raise an intentional exception, in the case of an error. To fix this with a simple solution, we can simply import [`abort`](https://flask.palletsprojects.com/en/1.0.x/api/?highlight=abort#flask.abort) from Flask:

```
from flask import abort
```

and we can call `abort(<status code>)`, e.g. with status code 500, `abort(500)` to rise an HTTPException for an Internal Server Error, in order to abort a request and prevent it from expecting a returned result. Since this is a course on web data modeling, we won't be going into errors in depth, but you can check out resources below.

#### expire_on_commit

Defaults to `True`. All instances will be fully expired after each commit(), so that all attrubute/object access subsequent to a competed transaction will load from the most recent database state.

```python
# change the default setting
db = SQLAlchemy(app, session_options={"expire_on_commit": False})
```

#### Resources on Error Handling

- [Flask Docs on Application Errors](https://flask.palletsprojects.com/en/1.0.x/errorhandling/)
- [Error Handling in Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling)

#### Code (with corrections)

```
from flask import Flask, render_template, abort

# ...

@app.route('/todos/create', method=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.form.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)
```



## 6 - Migrations

### Introduction - Migrations Part 1

<iframe width="770" height="433" src="https://www.youtube.com/embed/Sr-QQluNUFo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

- **Migrations** deal with how we manage modifications to our data schema, over time.
- Mistakes to our database schema are very expensive to make. The entire app can go down, so we want to
  - quickly roll back changes, and
  - test changes before we make them
- A migration is a file that keep track of changes to our database schema (structure of our database).
  - Offers **version control** on our schema.

#### Upgrades and rollbacks

- Migrations stack together in order to form the latest version of our database schema
- We can **upgrade** our database schema by **applying migrations**
- We can **roll back** our database schema to a former version by reverting migrations that we applied

### Migrations Part 2

<iframe width="770" height="433" src="https://www.youtube.com/embed/j1_unrCqU7k" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Migrations

- encapsulate a set of changes to our database schema, made over time.
- are uniquely named
- are usually stored as *local files* in our project repo, e.g. a `migrations/` folder
- There should be a 1-1 mapping between the changes made to our database, and the *migration files* that exist in our migrations/ folder.
- Our migrations files set up the tables for our database.
- All changes made to our db should exist physically as part of migration files in our repository.

#### 3 types of scripts

- **migrate**: creating a migration script template to fill out; generating a migration file based on changes to be made
- **upgrade**: applying migrations that hadn't been applied yet ("upgrading" our database)
- **downgrade**: rolling back applied migrations that were problematic ("downgrading" our database)

#### Flask-Migrate & Flask-Script

- **Flask-Migrate** (flask_migrate) is our migration manager for migrating SQLALchemy-based database changes
- **Flask-Script** (flask_script) lets us run migration scripts we defined, from the terminal

#### Steps to get migrations going

1. Initialize the migration repository structure for storing migrations
2. Create a migration script (using Flask-Migrate)
3. (Manually) Run the migration script (using Flask-Script)

<iframe width="770" height="433" src="https://www.youtube.com/embed/3vlK5FUdW_I" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Flask-Migrate

<iframe width="770" height="433" src="https://www.youtube.com/embed/bwPUM16rtFE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Links:

- [Flask-Migrate documentation](https://flask-migrate.readthedocs.io/en/latest/)
- [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/)

#### Importing `Migrate` and creating `Migrate` instance

```python
from flask_migrate import Migrate

migration = Migrate(app, db)
```

#### Creating `migrations` dir using `flask db init`

```shell
# flask db init
/root/pyenvs/fullstack/lib/python3.7/site-packages/flask_sqlalchemy/__init__.py:834: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
  Creating directory /root/fs_ex/todo/migrations ...  done
  Creating directory /root/fs_ex/todo/migrations/versions ...  done
  Generating /root/fs_ex/todo/migrations/README ...  done
  Generating /root/fs_ex/todo/migrations/env.py ...  done
  Generating /root/fs_ex/todo/migrations/script.py.mako ...  done
  Generating /root/fs_ex/todo/migrations/alembic.ini ...  done
  Please edit configuration/connection/logging settings in '/root/fs_ex/todo/migrations/alembic.ini' before
  proceeding.
```

<iframe width="770" height="433" src="https://www.youtube.com/embed/lTgA05lcIHA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Syncing models using `flask db migrate`

<iframe width="770" height="433" src="https://www.youtube.com/embed/H-PWJ5p-SpM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

```shell
# flask db migrate
/root/pyenvs/fullstack/lib/python3.7/site-packages/flask_sqlalchemy/__init__.py:834: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'todo'
  Generating /root/fs_ex/todo/migrations/versions/8938cfaeed68_.py ...  done
```



#### `flask db upgrade` and `flask db downgrade`

<iframe width="770" height="433" src="https://www.youtube.com/embed/sysYabvXRCs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

```shell
# flask db upgrade
/root/pyenvs/fullstack/lib/python3.7/site-packages/flask_sqlalchemy/__init__.py:834: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 8938cfaeed68, empty message
```



#### Adding the `completed` column to test migration

<iframe width="770" height="433" src="https://www.youtube.com/embed/UVIhJ_qZzAA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

```shell
# flask db migrate    
/root/pyenvs/fullstack/lib/python3.7/site-packages/flask_sqlalchemy/__init__.py:834: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.ddl.postgresql] Detected sequence named 'todo_id_seq' as owned by integer column 'todo(id)', assuming SERIAL and omitting
INFO  [alembic.autogenerate.compare] Detected added column 'todo.completed'
  Generating /root/fs_ex/todo/migrations/versions/3966764ac5bd_.py ...  done

root at lcw-linode in ~/fs_ex/todo (fullstack)
# flask db upgrade
/root/pyenvs/fullstack/lib/python3.7/site-packages/flask_sqlalchemy/__init__.py:834: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 8938cfaeed68 -> 3966764ac5bd, empty message
```

#### Workding with exsiting data

If we have some data in the table, and we are adding a new column to the table with `nullable=False`, there will be errors because the existing data violates that constraint.

```
sqlalchemy.exc.IntegrityError: (psycopg2.errors.NotNullViolation) column "completed" contains null values
```

What we need to do is to take care of the upgrade function like this:

```python
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # 1. we allow null values for column 'completed'
    op.add_column('todo', sa.Column('completed', sa.Boolean()))
    # ### end Alembic commands ###

    # 2. update the existing records to make values for 'completed' as 'false'
    op.execute("UPDATE todo SET completed = False WHERE completed IS NULL;")

    # 3. change nullable=False back to column 'completed'
    op.alter_column('todo', 'completed', nullable=False)
```

Now we `flask db upgrade`:

```shell
# flask db upgrade
/root/pyenvs/fullstack/lib/python3.7/site-packages/flask_sqlalchemy/__init__.py:834: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 8938cfaeed68 -> 3966764ac5bd, empty message
```

Double check the recrods in table `todo`:

```sql
todos=# select * from todo;
 id | description | completed 
----+-------------+-----------
  2 | todo 1      | f
  3 | todo 2      | f
(2 rows)
```

<iframe width="770" height="433" src="https://www.youtube.com/embed/2B4II_X-W0k" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



#### Overall Steps to Set Up & Run Migrations

1. **Bootstrap database migrate commands**: link to the Flask app models and database, link to command line scripts for running migrations, set up folders to store migrations (as versions of the database)
2. **Run initial migration to create tables for SQLAlchemy models**, recording the initial schema: ala git init && first git commit. Replaces use of db.create_all()
3. Migrate on changes to our data models
   - Make changes to the SQLAlchemy models
   - Allow Flask-Migrate to auto-generate a migration script based on the changes
   - Fine-tune the migration scripts
   - Run the migration, aka “upgrade” the database schema by a “version”

#### It’s always helpful to read the docs!

- https://alembic.sqlalchemy.org/en/latest/
- https://flask-migrate.readthedocs.io/en/latest/



## 7 - Build a CRUD App with SQLAlchemy ORM - Part 2

- Implementing update functionality: update a todo item's completed state
- Implementing delete functionality: remove a todo item
- Model relationships between objects in SQL and SQLAlchemy
  - Setting up Foreign Key constraints
- Building CRUD on Lists of To-Do items
- Handling the special case of modeling many-to-many relationships



### Updating a Todo Item

<iframe width="770" height="433" src="https://www.youtube.com/embed/0Xm2VnXRzVk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

An **update** involves setting the attributes of an existing object in the database.

In SQL:

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

In SQLAlchemy ORM:

```python
user = User.query.get(some_id)
user.name = 'Some new name'
db.session.commit()
```

<iframe width="770" height="433" src="https://www.youtube.com/embed/r-6MkZlDJ_8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

[Jinja Docs `if`](http://jinja.pocoo.org/docs/2.10/templates/#if)



#### Modifying the view in `index.html` to show checkboxes

<iframe width="770" height="433" src="https://www.youtube.com/embed/HAZwYPOZf3s" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



#### Having the checkboxes send off update (`POST`) requests

<iframe width="770" height="433" src="https://www.youtube.com/embed/20_s84r0j2Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



#### Defining the handler for the route

<iframe width="770" height="433" src="https://www.youtube.com/embed/fhtBPu5yGLw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



#### Fixing the ordering

<iframe width="770" height="433" src="https://www.youtube.com/embed/V2y8J81UEqw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



### Deleting a todo item

<iframe width="770" height="433" src="https://www.youtube.com/embed/23WUhMIaP9c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

In SQL:

```
DELETE FROM table_name
WHERE condition;
```

In SQLAlchemy ORM:

```py
todo = Todo.query.get(todo_id) 
db.session.delete(todo) # or...
Todo.query.filter_by(id=todo_id).delete()
db.session.commit()
```

#### Steps we'll implement:

- Show a delete button for each TODO item
- Pressing the delete button sends a request that includes which to-do item to delete
- The controller takes the user input, and notifies the models to delete the To-Do object by ID
- On successful deletion by the models, the controller should notify the view to refresh the page and redirect to our homepage, showing a fresh fetch of all To-Do items to now exclude the removed item.

#### Using the DELETE method

Requests that delete objects should use the method `DELETE`, as opposed to `POST`, `GET`, etc. when sending requests to the server.

<iframe width="770" height="433" src="https://www.youtube.com/embed/a43M8qRSGXE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Introduction: Modeling Relationships

<iframe width="770" height="433" src="https://www.youtube.com/embed/Fjb8gYBA170" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Review: Relationships & Joins

<iframe width="770" height="433" src="https://www.youtube.com/embed/RgOXSZhYVe4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

A foreign key is stored in a child table, which retrieves the primary key in the parent table. A child object belongs to a parent object through the foreign key that's stored on the child table.

behicles: Child																						drivers: Parent

| id   | make     | model  | year | driver_id | id   | name   | state |
| ---- | -------- | ------ | ---- | --------- | ---- | ------ | ----- |
| 1    | Nissan   | Altima | 2018 | 3         | 1    | Amy    | NE    |
| 2    | Toyota   | Camry  | 2018 | 4         | 2    | Bob    | NE    |
| 3    | Kawasaki | Ninja  | 2018 | 3         | 3    | Sarah  | NE    |
| 4    | Honda    | Civic  | 2018 | 2         | 4    | Aditya | NE    |

```sql
SELECT make, model, year FROM behicle
JOIN drivers
ON vehicles.driver_id = drivers.id
WHERE drivers.name = 'Sarah';
```

### db.relationship

<iframe width="770" height="433" src="https://www.youtube.com/embed/WULi0shD61Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

![img](https://video.udacity-data.com/topher/2019/August/5d5f5ed0_screen-shot-2019-08-22-at-8.34.29-pm/screen-shot-2019-08-22-at-8.34.29-pm.png)

### Configuring Relationships

<iframe width="770" height="433" src="https://www.youtube.com/embed/QATpsBELc8s" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Lazy loading vs. Eager loading

<iframe width="770" height="433" src="https://www.youtube.com/embed/oq-Wqp_BSps" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

See [the SQLAlchemy Docs on Relationship Loading Techniques](https://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html) for more loading options.

#### Other relationship options: `collection_class` and `cascade`

<iframe width="770" height="433" src="https://www.youtube.com/embed/qywsiQi6lvk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

[SQLALchemy ORM Relationship Docs](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship)

### Setting up the Foreign Key Constraint

<iframe width="770" height="433" src="https://www.youtube.com/embed/ovI5b7j-Oqc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

- `db.relationship` does *not* set up foreign key constraints for you. We need to add a column, `some_parent_id`, on the **child** model that has a foreign key constraint
- Whereas we set `db.relationship` on the **parent** model, we set the foreign key constraint on the **child** model.
- A foreign key constraint prefers **referential integrity** from one table to another, by ensuring that the foreign key column always maps a primary key in the foreign table.

![img](https://video.udacity-data.com/topher/2019/August/5d5f62cd_screen-shot-2019-08-22-at-8.51.27-pm/screen-shot-2019-08-22-at-8.51.27-pm.png)

#### `db.ForeignKey` question

<iframe width="770" height="433" src="https://www.youtube.com/embed/oVuHm3rNxKI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

##### `db.ForeignKey`

- Option in db.column to specify a foreign key constraint, referring to the primary key of the other table / model
- Gets defined on the Child model

![img](https://video.udacity-data.com/topher/2019/August/5d5faa19_screen-shot-2019-08-23-at-1.55.35-am/screen-shot-2019-08-23-at-1.55.35-am.png)

<iframe width="770" height="433" src="https://www.youtube.com/embed/XXy8hL0d30c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<iframe width="770" height="433" src="https://www.youtube.com/embed/Wd9zyi8dCGM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### One-to-Many Relationship Setup

 ["The 3 Types of Relationships in Database Design" by Database.Guide -- click here](https://database.guide/the-3-types-of-relationships-in-database-design/)

#### Creating the `TodoList` model and adding the foreign key to the child `Todo` model

<iframe width="770" height="433" src="https://www.youtube.com/embed/5Bl9RtsEtAY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

#### Overall steps taken

- Modified our Todo model to (temporarily) allow null values in `list_id`:

  ```py
  list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=True)
  ```

- Ran the migration, allowing `list_id` to be null

Then using psql (or any other Postgres client),

- Populated our database with a default list ("Uncategorized") to add all currently existing Todo items to
- Associated existing to-do items with the "Uncategorized" list with ID 1, setting todo.list_id = 1. We could have also done this in a migration rather than using psql; either works.
- Set `nullable=False` on the `list_id` column
- Ran `flask db migrate` to generate a migration file for updating the nullability constraint
- Ran `flask db upgrade` to apply the migration

#### Example Terminal Output

```bash
macbook:~ amy$ psql todoapp
psql (11.3, server 10.10)
Type "help" for help.
todoapp=# \dt
            List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+-------
 public | alembic_version | table | amy
 public | todolists       | table | amy
 public | todos           | table | amy
(3 rows)

todoapp=# insert into todolists (name) values ('Uncategorized');
INSERT 0 1
todoapp=# update todos set list_id = 1 where list_id is null;
UPDATE 6
todoapp=# select * from todos;
 id | description  | completed | list_id
----+--------------+-----------+---------
  5 | Do homework  | f         |       1
  7 | Do thing 3   | f         |       1
 21 | thing 17     | t         |       1
  6 | Do a thing   | t         |       1
  8 | Do a thing 4 | t         |       1
  9 | Thing 5      | f         |       1
(6 rows)

todoapp=# \q
```

### CRUD on List of To-Dos

<iframe width="770" height="433" src="https://www.youtube.com/embed/Q2JlOnmxVcE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
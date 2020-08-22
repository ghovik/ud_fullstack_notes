import sys
from flask import Flask, request, redirect, url_for, jsonify, abort
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey

app = Flask(__name__)

uri = "postgresql://postgres:postgres@localhost:5432/todos"
app.config["SQLALCHEMY_DATABASE_URI"] = uri
# define our database
db = SQLAlchemy(app)
# define migration
migration = Migrate(app, db)

class TodoList(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    todo = db.relationship("Todo", backref="todolist", lazy=True)

class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)
    todolist_id = db.Column(db.Integer, db.ForeignKey("todolist.id"))

    def __repr__(self):
        return f"<Todo {self.id} {self.description}>"

# create schema if not exist
# db.create_all()

@app.route("/")
def index():
    return render_template(
        "index.html", 
        data=Todo.query.order_by("id").all())

# @app.route("/todo/create", methods=["POST"])
# def create():
#     todo = request.form.get("todo", "")
#     rec = Todo(description=todo)
#     db.session.add(rec)
#     db.session.commit()
#     db.session.close()
#     return redirect(url_for("index"))
    # here index is the name of the function index()

@app.route("/todo/create", methods=["POST"])
def create():
    # request.get_json() is from 
    # {"description": document.getElementById("todo").value},
    # which is a dict
    err = 0 # err flag
    todo = request.get_json()["description"]
    # rec = Todo(description=todo)
    try:
        rec = Todo(description=todo)
        db.session.add(rec)
        db.session.commit()
    except Exception as e:
        err = 1
        db.session.rollback()
        print(f"err:\n{e}")
    finally:
        db.session.close()
    if not err:
        return jsonify({"description": todo})
    abort (400)

# UPDATE
# the item inside a <> block becomes an input argument to this function
# when the html sents a post request to "/todo/3/set-completed", 3 will be
# assigned to todo_id
@app.route("/todo/<todo_id>/set-completed", methods=["POST"])
def todo_checked(todo_id):
    completed = request.get_json()["completed"]
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"error:\n{e}")
    finally:
        db.session.close()
    return redirect(url_for("index"))

# Delete
@app.route("/todo/delete/<todo_id>", methods=["DELETE"])
def todo_deleted(todo_id):
    try:
        item_to_delete = Todo.query.get(todo_id)
        db.session.delete(item_to_delete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"err:\n{e}")
    finally:
        db.session.close()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)

from enum import unique
from flask import Flask, request, redirect, url_for, jsonify, abort
from flask import json
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


# --------------------- many-to-many example -------------------------
order_items = db.Table(
    "order_items",
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True)
    )

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)
    products = db.relationship(
        "Product", secondary=order_items, backref=db.backref("orders"), lazy=True)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
# --------------------- many-to-many example -------------------------

class TodoList(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
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

# create a new todo item and show corresponding list
@app.route("/lists/<list_id>")
def get_list_todos(list_id):
    return render_template("index.html",
        lists=TodoList.query.all(),
        active_list=TodoList.query.filter_by(id=list_id).first(),
        todos=Todo.query.filter_by(todolist_id=list_id).order_by("id")
        )


# Create a new list
@app.route("/lists/create", methods=["POST"])
def create_a_list():
    list_name = request.get_json()["list_name"]
    new_list = TodoList(name=list_name)
    err = 0
    try:
        db.session.add(new_list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"err:\n{e}")
        err = 1
    finally:
        db.session.close()
    if not err:
        new_list_id = TodoList.query.filter_by(name=list_name).first().id
        return jsonify({"success": True, "list_id": new_list_id})


@app.route("/")
def index():
    return redirect(url_for("get_list_todos", list_id=1))


# create a todo item
@app.route("/todo/create", methods=["POST"])
def create():
    # request.get_json() is from 
    # {"description": document.getElementById("todo").value},
    # which is a dict
    err = 0 # err flag
    todo = request.get_json()
    # rec = Todo(description=todo)
    try:
        rec = Todo(
            description=todo["description"], 
            todolist_id=todo["list_id"])
        db.session.add(rec)
        db.session.commit()
    except Exception as e:
        err = 1
        db.session.rollback()
        print(f"err:\n{e}")
    finally:
        db.session.close()
    if not err:
        return jsonify({
            "description": todo["description"],
            "list_id": todo["list_id"]})
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
        list_id = item_to_delete.todolist_id
        db.session.delete(item_to_delete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"err:\n{e}")
    finally:
        db.session.close()
    return jsonify({"success": True, "list_id": list_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)

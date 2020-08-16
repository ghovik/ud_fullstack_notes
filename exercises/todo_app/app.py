from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

"""
"R" in CRUD:
Replace data in index() to real data from db
1.  
"""

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

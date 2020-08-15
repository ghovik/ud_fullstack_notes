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
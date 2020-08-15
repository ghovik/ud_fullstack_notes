from flask import Flask
from flask.templating import render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html", 
        data=[{"description": f"Todo {i}"} for i in range(1, 4)])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)

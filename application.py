from flask import Flask
from models import *

app = Flask(__name__)

@app.route("/")
def histograms():
    return "Histograms go here"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
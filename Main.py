from flask import Flask, render_template
import database

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

app.run(debug=True)
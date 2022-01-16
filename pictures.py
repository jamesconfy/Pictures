from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Dashboard')


if __name__ == "__main__":
    app.run()
from flask import Flask, render_template, request, flash, redirect, url_for
from forms import ImageForm
import os
from utils import save_image
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

DB_PASS = os.environ.get('DB_PASS')
DB_USER = os.environ.get('DB_USER')
DB_HOST = os.environ.get('DB_HOST')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/pictures'

db = SQLAlchemy(app)

class ImageFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(120), default=datetime.utcnow)
    image_file = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User('{self.image_file}')"

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    images = ImageFile.query.order_by(ImageFile.date_created.desc()).paginate(per_page=3, page=page)
    return render_template('home.html', title='Dashboard', images=images)

@app.route("/upload", methods=["POST", "GET"])
def uploadImage():
    form = ImageForm()
    if request.method =='POST':
        if form.validate_on_submit():
            imgFile = save_image(form.img.data)
            pic = ImageFile(image_file=imgFile)
            db.session.add(pic)
            db.session.commit()
            flash(f'Image Uploaded Successfully')
            return redirect(url_for('home'))

        flash(f'The file {form.img.data} is invalid')
    return render_template("upload.html", form=form, title="Upload Image")

@app.route("/delete")
def deleteImage():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(db.create_all())
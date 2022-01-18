from flask import render_template, request, flash, redirect, url_for
from pictures import app, db
from pictures.forms import ImageForm
from pictures.utils import save_image
from pictures.models import ImageFile

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
            flash(f'Image Uploaded Successfully', 'success')
            return redirect(url_for('home'))

        flash(f'The file is invalid', 'danger')
    return render_template("upload.html", form=form, title="Upload Image")

@app.route("/view/<int:id>")
def viewImage(id):
    image = ImageFile.query.get_or_404(id)
    return render_template('view.html', image=image, title=image.id)

@app.route("/delete/<id>")
def deleteImage(id):
    image = ImageFile.query.get_or_404(id)

    db.session.delete(image)
    db.session.commit()
    flash(f'Image Deleted Successfully', 'info')
    return redirect(url_for('home'))

@app.route("/modify/<int:id>", methods=["POST", "GET"])
def modifyImage(id):
    image = ImageFile.query.get_or_404(id)

    form = ImageForm()
    if request.method =='POST':
        if form.validate_on_submit():
            imgFile = form.img.data
            if imgFile:
                imgFile2 = save_image(form.img.data)
            else:
                imgFile2 = image.image_file

            image.image_file = imgFile2
            db.session.commit()
            flash(f'Image Modified Successfully', 'success')
            return redirect(url_for('home'))

        flash(f'The file {form.img.data} is invalid')
    return render_template("upload.html", form=form, title="Modify Image")

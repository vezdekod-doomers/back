import io
from io import BytesIO
from flask import Flask, request, send_file, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGBLOB
from PIL import Image
from hash import phash

basedir = 'mysql://root:example@db:3306/mysql'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = basedir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class FileContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary().with_variant(LONGBLOB, "mysql"), nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    aspect = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.LargeBinary(), nullable=False)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    data = file.read()
    image = Image.open(io.BytesIO(data))
    width, height = image.size
    aspect_ratio = width / height
    image_hash = phash(image)
    thumb_image = FileContent.query.filter(FileContent.hash == image_hash)\
        .filter(FileContent.aspect == int(aspect_ratio * 100))\
        .first()

    if thumb_image is not None:
        if thumb_image.width <= width or thumb_image.height <= height:
            thumb_image.data = data
            thumb_image.width = width
            thumb_image.height = height
            db.session.commit()
        resp = make_response(str(thumb_image.id), 200)
        resp.mimetype = "text/plain"
        return resp

    newFile = FileContent(data=data, aspect=int(aspect_ratio * 100), hash=image_hash, width=width, height=height)
    db.session.add(newFile)
    db.session.commit()
    resp = make_response(str(newFile.id), 200)
    resp.mimetype = "text/plain"
    return resp


@app.route('/get/<int:file_id>')
def download(file_id):
    file_data = FileContent.query.get(file_id)
    if file_data is None:
        return make_response('', 404)

    scale = 1.0
    if request.args.get('scale') is not None:
        scale = float(request.args.get('scale'))

    image = Image.open(io.BytesIO(file_data.data))
    width, height = image.size
    image = image.resize([int(width * scale), int(height * scale)], Image.ANTIALIAS)
    out_img = io.BytesIO()
    image.save(out_img, format='JPEG')
    return send_file(BytesIO(out_img.getvalue()), attachment_filename='out.jpg', as_attachment=True)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

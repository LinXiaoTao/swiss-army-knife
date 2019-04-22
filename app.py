from flask import Flask, request, url_for, send_file
import qrcode
from werkzeug.utils import secure_filename
from os import path
import os
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/file2qrcode', methods=['POST'])
def file_to_qrcode():
    try:
        upload_file = request.files['file']
        if not upload_file:
            return "没有上传文件"
        file_name = secure_filename(upload_file.filename)
        app.logger.info("upload file: %s", file_name)
        if not path.exists('./static/apk'):
            os.mkdir('./static/apk')
        if not path.exists('./static/qrcode'):
            os.mkdir('./static/qrcode')
        file_path = './static/apk/' + file_name
        upload_file.save(file_path)
        result = url_for('.static', _external=True, filename='apk/' + file_name)
        basename = path.splitext(file_name)[0]
        qrcode_file_path = './static/qrcode/' + basename + ".png"
        qrcode.make(result).save(qrcode_file_path)
        return json.dumps(
            {'code': 0, 'data': url_for('.static', _external=True, filename='qrcode/' + basename + ".png")}
        )
    except Exception as e:
        app.logger.error("file2qrcode error: %s", e)
        return json.dumps(
            {'code': 1000}
        )


if __name__ == '__main__':
    app.run()

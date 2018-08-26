# -*- coding: utf-8 -*-

from flask import Flask,render_template,request,redirect,url_for,flash,make_response,send_from_directory
from werkzeug.utils import secure_filename
import os
import sys
from flask_uploads import UploadSet, configure_uploads, ALL
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__),'static','uploads')
# files = UploadSet('files', ALL)
# app.config['UPLOADS_DEFAULT_DEST'] = 'static/uploads'

# configure_uploads(app, files)

ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload/',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择任何文件！','err')
            return redirect(url_for('upload'))
        f = request.files['file']
        print (f)
        if f and allowed_file(f.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            upload_file_name = os.path.join(app.config['UPLOAD_FOLDER'],f.filename)
            print(secure_filename(f.filename))
            f.save(upload_file_name)
            flash("文件上传成功", 'ok')
            return redirect(url_for('upload'))
        flash("文件上传失败，无效的格式 %s" % f.filename.rsplit('.', 1)[1],'err')
        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.route('/file_list/')
def file_list():
    content = {}
    for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        print (root, dirs, files)
        for filename in files:
            filepath = os.path.join(root, filename)
            content[filename] = os.path.getsize(filepath)/1024
    return render_template('file_list.html', files = content)


@app.route('/download/')
def download():
    """ 下载附件、预览文本文件
    :catalog(str):  下载分类(子)目录，比如attachment、script
    :filename(str): 下载的实际文件(不需要目录，目录由catalog指定)，包含扩展名
    """
    # 下载文件存放目录
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    # 下载分类(directory的子目录)
    catalog = request.args.get("catalog")
    # 下载文件名
    filename = request.args.get("filename")
    app.logger.debug("Want to download a file with catalog: {0}, filename: {1}".format(catalog, filename))
    if catalog and filename:
        if filename.split(".")[-1] in ("txt", "sh", "py", "php"):
            headers = ("Content-Type", "text/plain;charset=utf-8;")
            as_attachment = False
        else:
            headers = ("Content-Disposition", "attachment;filename={}".format(filename))
            as_attachment = True
        if os.path.isfile(os.path.join(directory, catalog, filename)):
            response = make_response(send_from_directory(directory=os.path.join(directory, catalog), filename=filename, as_attachment=as_attachment))
            response.headers[headers[0]] = headers[1]
        else:
            response = make_response("Not Found File")
    else:
        response = make_response("Invalid Download Request")
    return response


if __name__ == '__main__':
    app.secret_key = '123456'
    app.run(debug=True,host='0.0.0.0')
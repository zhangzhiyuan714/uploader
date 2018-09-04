#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:45
# @File    : Views.py
"""
视图模型
"""
 
from  flask import render_template,Blueprint,redirect,url_for,flash,request
from Start import login_manger
from Form import Login_Form,Register_Form
from Model import  Users
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
from Start import db
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'gif'])
root_path = os.path.join(os.path.dirname(__file__),'static','uploads')


def allowed_file(filename):
    return True
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


blog=Blueprint('blog',__name__)  #蓝图

@blog.route('/')
def index():
    # form=Login_Form()
    return render_template('welcome.html')
 
@blog.route('/index')
def l_index():
    form = Login_Form()
    return render_template('login.html',form=form)
 
@blog.route('/login',methods=['GET','POST'])
def login():
        form=Login_Form()
        if form.validate_on_submit():
            user=Users.query.filter_by(name=form.name.data).first()
            if user is not  None and user.pwd==form.pwd.data:
                login_user(user)
                flash('登录成功')
                return  render_template('ok.html',name=form.name.data)
            else:
                flash('用户或密码错误')
                return render_template('login.html',form=form)
        return render_template('login.html',form=form)
 
#用户登出
@blog.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('blog.index'))
 
 
@blog.route('/register',methods=['GET','POST'])
def register():
    form=Register_Form()
    if form.validate_on_submit():
        user=Users(name=form.name.data,pwd=form.pwd.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('blog.index'))
    return render_template('register.html',form=form)

@blog.route('/upload/',methods=['GET','POST'], )
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择任何文件！','err')
            return redirect(url_for('blog.upload'))
        f = request.files['file']
        print (f)
        if f and allowed_file(f.filename):
            if not os.path.exists(root_path):
                os.makedirs(root_path)
            upload_file_name = os.path.join(root_path,f.filename)
            print(secure_filename(f.filename))
            f.save(upload_file_name)
            flash("文件上传成功", 'ok')
            return redirect(url_for('blog.upload'))
        flash("文件上传失败，无效的格式 %s" % f.filename.rsplit('.', 1)[1],'err')
        return redirect(url_for('blog.upload'))
    return render_template('upload.html')

@blog.route('/filelist/')
@login_required
def filelist():
    content = {}
    for root, dirs, files in os.walk(root_path):
        print (root, dirs, files)
        for filename in files:
            filepath = os.path.join(root, filename)
            content[filename] = os.path.getsize(filepath)/1024
    return render_template('filelist.html', files = content)


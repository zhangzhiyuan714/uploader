#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:45
# @File    : Model.py
"""
数据模型
"""
 
 
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
from Start import login_manger
from Start import db
 
class Users(UserMixin,db.Model):
    __tablename__ = 'acount'#对应mysql数据库表
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    pwd = db.Column(db.String(64), unique=True, index=True)
    def __init__(self,name,pwd):
        self.name=name
        self.pwd=pwd
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % self.name
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False


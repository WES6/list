# -*- coding: utf-8 -*-
import jieba as jieba
import requests
from bs4 import BeautifulSoup
from flask import url_for, request, flash, render_template, json
from flask_admin import BaseView, expose
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import BaseForm
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from wtforms import StringField

from app import admin, db
from app.main import main
from app.models import User, Comment, Original


# class LaView(ModelView):
#     column_searchable_list = ['user_name']
#
#     def is_accessible(self):
#         if not current_user.is_authenticated():
#             return False
#         else:
#             return current_user.user_name == ('admin')
#
#     def inaccessible_callback(self, name, **kwargs):
#         # redirect to login page if user doesn't have access
#         return redirect(url_for('auth.login', next=request.url))


# admin.add_view(LaView(User, db.session))


# class AlertView(ModelView):
#     @expose('/')
#     @login_required
#     def index(self):
#         return self.render('alert/alert.html')

# class al_BrandForm(BaseForm):
#     al_name = StringField()


class CommentView(ModelView):
    column_searchable_list = ['comment_name']

    def is_accessible(self):
        return current_user.is_authenticated()

    # 不显示主键
    column_display_pk = False
    # 可以查看详情
    can_view_details = True
    # 不可以创建
    can_create = False
    # 每页显示几条
    page_size = 10

    column_exclude_list = ['comment_text', ]
    # column_labels = {
    #     'message_name': u'信息名称',
    #     'message_add': u'信息地址'
    # }

    # 覆写form
    # form = al_BrandForm


admin.add_view(CommentView(Comment, db.session))
# name='Alert', endpoint='alert'


class OriginalView(ModelView):

    def is_accessible(self):
        if current_user.role > 2:
            return True

    column_searchable_list = ['original_name']
    # 不显示主键
    column_display_pk = False
    # 可以查看详情
    can_view_details = True
    # 不可以创建
    can_create = False
    # 每页显示几条
    page_size = 10

    column_exclude_list = ['original_text', ]
    # column_labels = {
    #     'message_name': u'信息名称',
    #     'message_add': u'信息地址'
    # }

    # 覆写form
    # form = al_BrandForm


admin.add_view(OriginalView(Original, db.session))


class CommentShowView(BaseView):

    def is_accessible(self):
        return current_user.is_authenticated()

    @expose('/')
    def index(self):

        dic = {}
        comments = Comment.query.all()
        t = ""
        for y in comments:
            t += y.comment_text
        seg_list = jieba.cut(t, cut_all=False)
        for i in seg_list:
            if i in dic:
                dic[i] += 1
            else:
                dic[i] = 1

        pao = [' ', '的', '“', '”', '也', '对', '年', '有', '了', '在', '和', '是', '，', '。', '月', '：', '、', '将', '等', '为', '不']
        for tyy in dic.items():
            if tyy[0] in pao:
                dic.pop(tyy[0])

        top = {}
        ee = dic.values()
        ee.sort(reverse=True)
        se = ee[1:11]
        for eee in dic.items():
            if eee[1] in se:
                top[eee[0]] = eee[1]
        keys = top.keys()[:10]
        values = top.values()[:10]

        dicc = []
        for kk in dic.items():
            dicc.append({'name': kk[0], 'value': kk[1]})
        print(dicc)

        return self.render('alert/alert_c.html', keys=json.dumps(keys), values=values, datas=json.dumps(dicc[:5000]))


admin.add_view(CommentShowView(name='CommentShow'))


class OriginalShowView(BaseView):

    def is_accessible(self):
        if current_user.role > 2:
            return True

    @expose('/')
    def index(self):
        dic = {}
        originals = Original.query.all()
        t = ""
        for y in originals:
            t += y.original_text
        seg_list = jieba.cut(t, cut_all=False)
        for i in seg_list:
            if i in dic:
                dic[i] += 1
            else:
                dic[i] = 1

        pao = [' ', '的', '“', '”', '也', '对', '年', '有', '了', '在', '和', '是', '，', '。', '月', '：', '、', '将', '等', '为', '不']
        for tyy in dic.items():
            if tyy[0] in pao:
                dic.pop(tyy[0])

        top = {}
        ee = dic.values()
        ee.sort(reverse=True)
        se = ee[:10]
        for eee in dic.items():
            if eee[1] in se:
                top[eee[0]] = eee[1]
        keys = top.keys()[:10]
        values = top.values()[:10]

        dicc = []
        for kk in dic.items():
            dicc.append({'name': kk[0], 'value': kk[1]})
        print(dicc)

        return self.render('alert/alert.html', keys=json.dumps(keys), values=values, datas=json.dumps(dicc[:5000]))


admin.add_view(OriginalShowView(name='OriginalShow'))


class UserView(ModelView):

    def is_accessible(self):
        if current_user.user_name == ('admin'):
            return True

    # 不显示主键
    column_display_pk = False
    # 可以查看详情
    can_view_details = True
    # 每页显示几条
    page_size = 10


admin.add_view(UserView(User, db.session))

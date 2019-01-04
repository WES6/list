# -*- coding: utf-8 -*-
import jieba
from flask import render_template

from app.alert import alert
from app.models import Comment


@alert.route('/c', methods=['GET'])
def c():
    dic = {}
    comments = Comment.query.all()
    t = ""
    for y in comments:
        t += y.original_text
    seg_list = jieba.cut(t, cut_all=False)
    for i in seg_list:
        if i in dic:
            dic[i] += 1
        else:
            dic[i] = 1
    print("666")
    print(dic)
    return render_template('alert/c.html')

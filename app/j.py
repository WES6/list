# -*- coding: utf-8 -*-
import jieba

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
for i in seg_list:
    print(i)

# coding: utf-8

def char_width(test_str):
	length = 0
	for char in test_str:
		# 汉字部分
		if u'\u4e00' <= char <= u'\u9fff':
			length += 2
		# 全角ASCII字符
		elif u'\uff01' <= char <= u'\uff5e':
			length += 2
		else:
			length += 1
	print length
	
char_width(u'中国')
char_width(u'ａｂ') # 不支持全角空格
char_width(u'a货')

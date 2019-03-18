# coding:utf-8
'''
重命名乱码的文件和文件夹
多半用来处理那些11区人压的沙雕压缩包
放到要转换的目录下，执行python rename_from_shj_to_gbk.py即可
Python 3.7.1测试通过
'''

import os, sys

from_codec = 'GBK'		# 从哪个编码开始转换
to_codec = 'Shift-JIS'	# 到哪个编码
		
# 用os.walk遍历目录（topdown表示从最深层开始遍历）
for root, dirs, files in os.walk(".", topdown=False):
	# 重命名文件
	for name in files:
		to_name = name.encode(from_codec).decode(to_codec)
		print(name, "=>", to_name)
		os.rename(os.path.join(root, name), os.path.join(root, to_name))
	
	# 重命名文件夹
	for name in dirs:
		to_name = name.encode(from_codec).decode(to_codec)
		print(name, "=>", to_name)
		os.rename(os.path.join(root, name), os.path.join(root, to_name))
# encoding: utf-8

# iOS数据处理用

# 读取如
# key1:string1
# key2:string2
# 这样的文件
# 转换成
# <key>key1</key>
# <string>value1</value>
# <key>key2</key>
# <string>value2</value>

import codecs

# 读取文件和输出文件
input = './input.txt'
output = './output.txt'

# key和value值指定
key_str = 'key'
value_str = 'string'

fin = codecs.open(input, 'r', 'utf-8')
fout = codecs.open(output, 'w', 'utf-8')

for eachline in fin.readlines():
	keyline = '<%s>%s</%s>\n' % (key_str, eachline.split(':')[0], key_str)
	valueline = '<%s>%s</%s>\n' % (value_str, eachline.split(':')[1][:-1], value_str)
	fout.write(keyline)
	fout.write(valueline)

fin.close()
fout.close()
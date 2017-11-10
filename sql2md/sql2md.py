# coding: utf-8

# 转换SQL代码至Markdown表格

import os
import sys
import codecs

class sql2md:
	# 表的某些信息
	table = {
		'name': '',
		'primary_key': '',
		'charset': '',
		'engine': '',
		'foreign_key_checks': ''
	}
	# 数据列宽度
	width = {
		'column': 6,
		'data_type': 10,
		'null': 4,
		'comment': 6
	}
	# 行内容
	line_content_list = []
	# 生成一些开始的内容
	def markdownInfo(self):
		output = u'* ' + self.table['name'] + u'\r\n' + \
				u'> 主键：    ' + self.table['primary_key'] + u'    \r\n' + \
				u'> 编码：    ' + self.table['charset'] + u'    \r\n' + \
				u'> 数据引擎：' + self.table['engine'] + u'    \r\n' + \
				u'> 外键检查：' + self.table['foreign_key_checks'] + u'    \r\n' + \
				'\r\n' # 再插入个换行，分割
				
		return output
	# 生成markdown表头
	def markdownTableHead(self):
		output = u'| 列名 ' + self.make_multi_char(' ', self.width['column'] - 6) + \
				u'| 数据类型 ' + self.make_multi_char(' ', self.width['data_type'] - 10) + \
				u'| 空 ' + self.make_multi_char(' ', self.width['null'] - 4) + \
				u'| 说明 ' + self.make_multi_char(' ', self.width['comment'] - 6) + u'|\r\n' + \
				u'|:' + self.make_multi_char('-', self.width['column'] - 1) + \
				u'|:' + self.make_multi_char('-', self.width['data_type'] - 1) + \
				u'|:' + self.make_multi_char('-', self.width['null'] - 1) + \
				u'|:' + self.make_multi_char('-', self.width['comment'] - 1) + u'|\r\n'
		return output
	# 生成markdown表本体
	def markdownTableBody(self):
		output = ''
		for line in self.line_content_list:
			output += 	u'|' + line[0] + self.make_multi_char(' ', self.width['column'] - self.char_width(line[0])) + \
						u'|' + line[1] + self.make_multi_char(' ', self.width['data_type'] - self.char_width(line[1])) + \
						u'|' + line[2] + self.make_multi_char(' ', self.width['null'] - self.char_width(line[2])) + \
						u'|' + line[3] + self.make_multi_char(' ', self.width['comment'] - self.char_width(line[3])) + u'|\r\n'
		return output
	# 读入sql文件
	def readSQLFile(self, file):
		in_comment = False

		with codecs.open(file, mode='r', encoding='utf-8') as f:
			# writeFile = open('output.txt', mode='w')
			for line in f:
				if line[0:2] == '--':
					continue
				elif line[0:2] == '/*':
					in_comment = True
				elif line[0:2] == '*/':
					in_comment = False
				elif line[0:2] == '  ':
					if in_comment:
						continue
					if line[2] == '`':
						# -1是为了去掉换行符
						column_line = line[2:-1]
						print '[table line] => ' + column_line
						self.line_content_list.append(self.line_operate(column_line))
					else:
						self.table['primary_key'] = line[2 + len('PRIMARY KEY (`'):0 - len('`)\n')].decode('utf-8').encode('gbk')
						print '[primry key] => ' + self.table['primary_key']
					# writeFile.write(line[2:])
					
					# if 
					
				elif line[0:12] == 'CREATE TABLE':
					self.table['name'] = line[len('CREATE TABLE `'): 0 - len('` {\n')]
					print '[table name] => ' + self.table['name']
					
				elif line[0:2] == ') ':
					pretty_line = line[2:-2]
					pretty_line_array = pretty_line.split(' ')
					if len(pretty_line_array) == 4:
						self.table['charset'] = pretty_line_array[3].split('=')[1]
						self.table['engine'] = pretty_line_array[0].split('=')[1]
						for line in self.line_content_list:
							if len(line) == 4 and line[3] == 'AUTO_INCREMENT':
								line[3] = pretty_line_array[1]
								# 还需修改最后一列宽度
								if self.width['comment'] < self.char_width(line[3]):
									self.width['comment'] = self.char_width(line[3])
					elif len(pretty_line_array) == 3:
						self.table['charset'] = pretty_line_array[2].split('=')[1]
						self.table['engine'] = pretty_line_array[0].split('=')[1]
					print '[ db engine] => ' + self.table['engine']
					print '[df charset] => ' + self.table['charset']
			# writeFile.close()
	
	# 每行操作
	def line_operate(self, line):
		
	
		line_part = line[:-1].split(' ')
		column_name = line_part[0][1:-1]
		data_type = line_part[1]
		null = line_part[2] + ' ' + line_part[3]
		if line_part[3] == 'NUL':
			print line_part
		if len(line_part) == 4:
			comment = '-'
		elif len(line_part) == 6:
			comment = line_part[5][1:-1]
		elif len(line_part) == 5:
			comment = line_part[4]
			
		if self.width['column'] < self.char_width(column_name):
			self.width['column'] = self.char_width(column_name)
		if self.width['data_type'] < self.char_width(data_type):
			self.width['data_type'] = self.char_width(data_type)
		if self.width['null'] < self.char_width(null):
			self.width['null'] = self.char_width(null)
		if self.width['comment'] < self.char_width(comment):
			self.width['comment'] = self.char_width(comment)
		return [column_name, data_type, null, comment]
		
	# 返回字符宽度
	def char_width(self, test_str):
		length = 0
		# print type(test_str)
		for char in test_str:
			# 汉字部分
			if u'\u4e00' <= char <= u'\u9fff':
				length += 2
			# 全角ASCII字符
			elif u'\uff01' <= char <= u'\uff5e':
				length += 2
			else:
				length += 1
		return length
	
	# 生成若干个空格	
	def make_multi_char(self, char, num):
		if num < 0:
			num = 0
		return char.decode('utf-8') * num
def main():
	if len(sys.argv) >= 2: 
		input_file = sys.argv[1]
	else:
		input_file = None
		
	if len(sys.argv) >= 4 and sys.argv[2] == '-o':
		output_file = sys.argv[3]
	else:
		output_file = None

	if input_file and output_file:
		print('input file is: ' + input_file + ' output file is: ' + output_file)
		s2m = sql2md()
		s2m.readSQLFile(input_file)
		fp = codecs.open(output_file, mode='w', encoding='utf-8')
		fp.write(s2m.markdownInfo())
		fp.write(s2m.markdownTableHead())
		fp.write(s2m.markdownTableBody())
		fp.close()
		exit()
	else:
		print('-------SQL to markdown table version 0.0.1-------')
		print('    Usage: sql2md.py <sql_file> -o <output_file>')
		exit();
	
if __name__ == '__main__':
	main()
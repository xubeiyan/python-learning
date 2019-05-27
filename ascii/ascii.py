import sys, random, argparse
import numpy as np
import math
from PIL import Image

# 70 level of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0qLCJUYXzcvunxrjft/\|()1{}[]?-_+-<>i!lI;:,\"^`'. "

# 10 level of gray
gscale2 = "@%#*+=-:. "

def getAverageL(image):
	"""
	given PIL Image. return average value of grayscale value
	"""
	# get image as numpy array
	im = np.array(image)
	# get the dimension
	# print(im.shape)
	w, h = im.shape
	# get the average
	return np.average(im.reshape(w * h))
	
def convertImageAscii(filename, cols, scale, moreLevels):
	"""
	Given Image and dimensions(rows, cols), return an m*n list of image
	"""
	# declare global
	global gscale1, gscale2
	# open image and convert to grayscale
	image = Image.open(filename).convert('L')
	# store the image dimensions
	W, H = image.size[0], image.size[1]
	print("input image dims: %d x %d" % (W, H))
	# compute tile width
	w = W / cols
	# compute tile height based on the aspect ratio and scale of the front
	h = w / scale
	rows = int(H / h)

	print("cols: %d, rows: %d" % (cols, rows))
	print("tile dims: %d x %d" % (w, h))

	# check if image size is too small
	if cols > W or rows > H:
		print("Image too small for specified cols")
		exit(0)

	# an ASCII Image is a list of character strings
	aimg = []
	# generate the list of tile dimensions
	for j in range(rows):
		y1 = int(j*h)
		y2 = int((j+1)*h)
		# correct the last tile
		if j == rows - 1:
			y2 = H
		# append an empty string
		aimg.append("")
		for i in range(cols):
			# crop the image to fit the tile
			x1 = int(i*w)
			x2 = int((i+1)*w)
			# correct the last tile
			if i == cols - 1:
				x2 = W
			# crop the image to extract the tile into another Image object
			img = image.crop((x1, y1, x2, y2))
			# get the average luminance
			avg = int(getAverageL(img))
			# look up the character for grayscale value(avg)
			if moreLevels:
				gsval = gscale1[int((avg*69)/255)]
			else:
				gsval = gscale2[int((avg*9)/255)]
			# append the ASCII character to the string
			aimg[j] += gsval
	# return text image
	return aimg

# main() function
def main():
	# create parser
	descStr = "This program converts an image into ASCII art."
	parser = argparse.ArgumentParser(description=descStr)
	# add expected arguments
	parser.add_argument('--file', dest='imgFile', required=True)
	parser.add_argument('--scale', dest='scale', required=False)
	parser.add_argument('--out', dest='outFile', required=False)
	parser.add_argument('--cols', dest='cols', required=False)
	parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

	# parse arguments
	args = parser.parse_args()

	imgFile = args.imgFile
	# set output file
	outFile = 'out.txt'
	if args.outFile:
		outFile = args.outFile
	# set scale default as 0.43, which suits a Courier font
	scale = 0.43
	if args.scale:
		scale = args.scale
	# set cols
	cols = 80
	if args.cols:
		cols = int(args.cols)
	print("Generating ASCII art...")
	# convert image to ASCII text
	aimg = convertImageAscii(imgFile, cols, scale, args.moreLevels)

	# open a new text file
	f = open(outFile, 'w')
	# write each string in the list to the new file
	for row in aimg:
		f.write(row + '\n')
	# clean up
	f.close()
	print("ASCII art written to %s" % outFile)

# call main 
if __name__ == '__main__':
	main()

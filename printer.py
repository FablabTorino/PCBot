import mraa
import urllib
from urlparse import urlparse
from os.path import splitext
from Adafruit_Thermal import *
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = False

#open the serial port on TX RX on the edison
x=mraa.Uart(0)

#Instantiate the pronter
printer = Adafruit_Thermal("/dev/ttyMFD1", 19200, timeout=5)


def printImageByUrl (url):
	
	urlpath=urlparse(url)
	root, ext = splitext(urlpath.path)
	print root
	print ext

	
	filename='printfile'+ext
	urllib.urlretrieve(url, filename)


	#here I downscale the Image
	baseWidth = 384

	# Open the image file.
	img = Image.open(filename)


	# Calculate the height using the same aspect ratio
	widthPercent = (baseWidth / float(img.size[0]))
	height = int((float(img.size[1]) * float(widthPercent)))
	size = (baseWidth, height)


	newName="root"+"scaled"+ext
	try:
	    im =  Image.open(filename)
	except:
	    print "Unable to load image"


	try:
	    im.load()
	except IOError:
	    pass # You can always log it to logger


	#here I really scale the image
	im.thumbnail(size,Image.ANTIALIAS)
	im.save(newName)

	#print the image on the printer
	printer.printImage(Image.open(newName))

	#add some empty lines
	printer.feed(3

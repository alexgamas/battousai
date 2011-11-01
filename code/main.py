# -*- coding: utf-8 -*-

'''
                                BEGIN OF PROGRAM
----------------------------------------------------------------------------
AUTHOR     : Alex Gamas
MAIN GOAL  : Open an Image file and display this!
VERSION    : 0.0.2
USAGE TIPS :
----------------------------------------------------------------------------

'''
import battousaiUtil as util
import imageView as iv
import Image


print "+-----------------------------------------------------+"
print "|                    TECLAS DE USO                    |"
print "+-----------------------------------------------------+"
print "| A = Imagem anterior                                 |"
print "| D = Proxima imagem                                  |"
print "| R = Gravar campo de trabalho                        |"
print "| F = Delimitar campo de trabalho                     |"
print "| Q = Sair, mesmo que ESC                             |"
print "+-----------------------------------------------------+"
print "\n\n\n\n"

folder = "../in_images"

files = util.listFiles(folder)

for imgfile in files:
	image = Image.open(imgfile)
	if (image.size > (800, 600)):
		print "Image file: {fmt_filename:<30} Mode: {fmt_mode:<10} Size: {fmt_size}".format(fmt_filename = imgfile, fmt_mode = image.mode, fmt_size = image.size)
	

iv.ImageView(files);


'''END OF PROGRAM
'''  

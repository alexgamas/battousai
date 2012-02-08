'''
Created on 05/02/2012

@author: Kefler
'''


from Tkinter import * #from tkinter
import Image as imx

root = Tk()
z = imx.open('../in_images/video_frame126.png')
i = PhotoImage(z)
l = Label(root, image=i)
l.pack()



root.mainloop()
from turtle import shape
import cv2  # for image processing
import easygui  # to open the filebox
import numpy as np  # to store image
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import *

""" fileopenbox opens the box to choose file
and help us store file path as string """

ImagePath = ''
ReSized6 = ''


def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):

    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    ReSized1 = cv2.resize(originalmage, (1920, 1080))

    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (1920, 1080))

    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (1920, 1080))

    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    ReSized4 = cv2.resize(getEdge, (1920, 1080))

    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (1920, 1080))

    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (1920, 1080))

    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    plt.imshow(ReSized6)
    plt.show()

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    plt.show()


def save(ReSized6, ImagePath):

    newName = "cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newName + " at " + path
    tk.messagebox.showinfo(title=None, message=I)


top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image !')
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))

upload = Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady=50)
save1 = Button(top, text="Save cartoon image", command=lambda: save(ImagePath, ReSized6), padx=30, pady=5)
save1.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
save1.pack(side=TOP, pady=50)

top.mainloop()

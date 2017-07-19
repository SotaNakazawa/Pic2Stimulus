#!/usr/bin/python
#coding: UTF-8

import os
import numpy as np
import cv2
import glob
from PIL import Image, ImageDraw

class ImageIO:

	def getImagePath(self):
		#画像の入っているディレクトリの相対パス取得
		imgPath = input("Please enter the images Realtive path : ")
		return imgPath

	def getImage(self):
		#画像のカテゴリとgetImagePath()で取得したディレクトリ内の画像のパスを取得
		imgKind = input("What kind of image\nPlease enter the Category : ")
		imgDir = [r for r in glob.glob(path + "/*")]
		return imgDir, imgKind

	def diminishingImage(self):
		#getImage()の各画像を比率保持したまま長辺を450pxに縮小
		#縮小した画像を「カテゴリ名+通し番号.jpg」としてtempフォルダに書き出す
		global imgDir
		count = 1

		makeDir = "temp"
		if not os.path.isdir(makeDir):
			os.mkdir(makeDir)

		for image in imgDir:
			imgPIL = Image.open(image)
			imgPIL.thumbnail((450,450),Image.ANTIALIAS)
			if count < 10:
				imgPIL.save("temp/" + imgKind + "00" + str(count) + ".jpg")
			else:
				imgPIL.save("temp/" + imgKind + "0" + str(count) + ".jpg")
			count += 1
		return

	def getAllImage(self):
		#diminishingImage()で書き出した画像をの読み込み
		imgDir = [r for r in glob.glob("temp/*")]
		return imgDir

class DrawImage:

	def checkCompeleted(self):
		#すべての画像を縮小したのか確認
		check = None
		while check != "yes" or check != "no":
			if check == "yes":
				return "ok"
			elif check == "no":
				return "yet"
			else:
				check = input("Are all images Diminishing?\n   yes/no\n")

	def resizeImage(self):
		#450*450の白地背景に縮小した画像を貼り付ける
		#それをresizedフォルダに通し番号をつけて保存
		global imgDir
		count = 1

		makeDir = "resized"
		if not os.path.isdir(makeDir):
			os.mkdir(makeDir)

		for image in imgDir:
			imgCV2 = cv2.imread(image, 1)
			canvas = Image.new("RGB", (450,450), (255,255,255))
			draw = ImageDraw.Draw(canvas)
			height, width = imgCV2.shape[:2]
			imgPIL = Image.open(image)
			canvas.paste(imgPIL, (int((450-width)/2),int((450-height)/2)))

			if count < 10:
				canvas.save(makeDir + "/" + "00" + str(count) + ".jpg")
			elif count < 100:
				canvas.save(makeDir + "/" + "0" + str(count) + ".jpg")
			else:
				canvas.save(makeDir + "/" + str(count) + ".jpg")
			count += 1

		return print("Completed!")


IO = ImageIO()
Draw = DrawImage()
check = ""

while check != "ok":
	path = IO.getImagePath()
	inputImage = IO.getImage()
	imgDir = inputImage[0]
	imgKind = inputImage[1]
	IO.diminishingImage()

	check = Draw.checkCompeleted()
	if check == "ok":
		imgDir = IO.getAllImage()
		Draw.resizeImage() #実行されていない
	elif check == "yet":
		print("OK, Please continue working.")
	else:
		print("Cool it :(")
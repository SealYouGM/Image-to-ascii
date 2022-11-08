# This file will create multiple txt file for each frame of a video

import cv2
import os
from os import listdir
from Image_en_Ascii import image_to_ascii
from threading import Thread
import time as tm
from time import time
import shutil
import multiprocessing

alreadyTransformed = []

def VideoToFrame(Video_Path: str, Video_name: str, nameProject) -> None:
	"""
	:param Video_Path: Path de la video
	:param Video_name: Nom de la video dans le path
	:return: None
	"""
	capture = cv2.VideoCapture(f"{Video_Path}/{Video_name}")
	folderName = f"AllFrames_{nameProject}"

	if os.path.exists(folderName):
		shutil.rmtree(folderName)
	os.makedirs(folderName)

	i = 0
	while capture.isOpened():
		ret, frame = capture.read()
		if not ret:
			break
		cv2.imwrite(f"{folderName}/frame{i}.jpg", frame)
		i += 1
	
	capture.release()
	cv2.destroyAllWindows()
	
def FrameToAscii(ThreadName: str, nameProject: str, rangeFrame: list) -> None:
	"""
	Cette fonction permet de transformer chaque frame en ASCII
	:return: None
	"""

	folder = f"AllFrames_{nameProject}"
	Ascii_folder = f"AsciiImages_{nameProject}"

	if os.path.exists(Ascii_folder) == False:
		os.makedirs(Ascii_folder)
	listImages = os.listdir(folder)

	for i in range(rangeFrame[0], rangeFrame[1]):
		finale = image_to_ascii(f"{folder}/frame{i}.jpg", 10)
		with open(f"AsciiImages_{nameProject}/frame{i}ASCII.txt", "w", encoding="utf-8") as file:
			for ligne in finale:
				file.write(f"{ligne} \n")
				
def readVideo(nameProject: str) -> None:
	"""
	Cette fonction permet d'afficher la video à 30FPS
	:return: None
	"""
	nbFrame = len(os.listdir(f"AsciiImages_{nameProject}"))
	for i in range(nbFrame):
		if f"frame{i}ASCII.txt" in os.listdir(f"AsciiImages_{nameProject}"):
			with open(f"AsciiImages_{nameProject}/frame{i}ASCII.txt", "r", encoding="utf-8") as file:
				print(file.read())
				
				tm.sleep(1/35)
				os.system('cls')
		else:
			pass
				
def main():
	"""
	:return: None
	"""
	mode = input("Creer une nouvelle video [1] ou afficher la video deja existante [2]: ")
	nameProject = input("Nom de votre projet: ")

	if mode == "2":
		readVideo(nameProject)
	elif mode == "1":
		nomVideo = input("Nom de votre video: ")
		numberThread = int(input("Nombre de threads: "))

		VideoToFrame("C:/Users/Yassine/Documents/video", f"{nomVideo}.mp4", nameProject)


		folder = f"AllFrames_{nameProject}"
		nombreImages = len(os.listdir(folder))


		#USE MULTIPROCESSING INSTEAD (MY CPU 16 CORES)
		jobs = []
		debut = time()
		#Create (n) processes
		for i in range(numberThread):
			L = [i * nombreImages // numberThread, (i * nombreImages // numberThread) + nombreImages // numberThread]
			process = multiprocessing.Process(target=FrameToAscii, args=(f"Thread {i}", nameProject, L))
			process.start()
			jobs.append(process)

		#Finishes all the processes
		for process in jobs: 
			process.join()

		fin = time()

		print(f"Temps pour calculer: {fin - debut}")

if __name__ == "__main__":
    main()
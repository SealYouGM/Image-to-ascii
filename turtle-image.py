import pygame
import cv2
from PIL import Image
import numpy as np
import os
######################## Calcul du niveau de gris moyen ########################
def moyen_nuance_gris(case):

    bloc_image = np.array(case)
    w,h = bloc_image.shape

    moyenne =  np.average(bloc_image.reshape(w*h))
    #print("Moyenne de gris : %d" %moyenne)
    return(moyenne)

######################## TRANSFORMATION DE L'IMAGE EN TEXTE ########################
def image_to_ascii(fichier, gris_choix):
    image = Image.open(fichier, "r").convert("L") #Conversion en noir/blanc

    #print(gris_choix)
    W, H = image.size[0], image.size[1] #obtient largeur et hauteur de l'image
    ratio = H/W*0.45                    #0.45 est ajustable
    nbr_col = int(W/5)                  ### #nombre de caractères en largeur (la fration W/x est ajustable: 1 => 1pixel = 1caractère) ###
    nbr_ligne = int(ratio*nbr_col)      #nombre de caractères en hauter

    #print("Nombre de caractères ASCII %d x %d" %(nbr_ligne, nbr_col))   #affiche les nouvelles dimensions de l'image

    gris_choix= int(gris_choix)
    image_texte = []

    #dépend du choix de la nuance de gris
    if gris_choix == 10:
        nuance_gris = "@%#*+=-:. "
    elif gris_choix ==70:
        nuance_gris = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    ## séparation de l'image en bloc => chaque bloc sera transformé en un caractère parmi la nuance de gris choisie ##
    for i in range(nbr_ligne):
        y1 = int(i*H/nbr_ligne)           
        y2 = int((i+1)*H/nbr_ligne)   

        image_texte.append("")
        ligne = ""
        for j in range(nbr_col):

            x1 = int(j*W/nbr_col)
            x2 = int((j+1)*W/nbr_col)

            tuile = image.crop((x1,y1,x2,y2)) #création du bloc
            gris = moyen_nuance_gris(tuile) #obtien le niveau de gris moyen (allant de 0 à 255)
            character = nuance_gris[int(gris*(gris_choix-1)/255)] #prend un caractère parmi la nuance de gris

            ligne += character #ajout du caractère à la ligne

        image_texte[i] = ligne

    return(image_texte)
# Making canvas
screen = pygame.display.set_mode((500, 400))
 
# Setting Title
pygame.display.set_caption('Drawing to ASCII')
 
 
draw_on = False
last_pos = (0, 0)
 
# Radius of the Brush
radius = 2
screen.fill((255, 255, 255))
 
def roundline(canvas, color, start, end, radius=1):
    Xaxis = end[0]-start[0]
    Yaxis = end[1]-start[1]
    dist = max(abs(Xaxis), abs(Yaxis))
    for i in range(dist):
        x = int(start[0]+float(i)/dist*Xaxis)
        y = int(start[1]+float(i)/dist*Yaxis)
        pygame.draw.circle(canvas, color, (x, y), radius)
 
 
try:
    while True:
        event = pygame.event.wait()
         
        if event.type == pygame.QUIT:
            raise StopIteration
             
        if event.type == pygame.MOUSEBUTTONDOWN:         
            # Selecting random Color Code
            color = (0, 0, 0)
            # Draw a single circle wheneven mouse is clicked down.
            pygame.draw.circle(screen, color, event.pos, radius)
            draw_on = True
        # When mouse button released it will stop drawing   
        if event.type == pygame.MOUSEBUTTONUP:
            draw_on = False
            os.system("cls")
            
            pygame.image.save(screen, "frame.png")
            image = cv2.imread("frame.png")
            finale = image_to_ascii("frame.png", 10)
            with open(f"frame_en_ASCII.txt", "w", encoding="utf-8") as file:
                for ligne in finale:
                    file.write(f"{ligne} \n")
            with open(f"frame_en_ASCII.txt", "r", encoding="utf-8") as file:
                print(file.read())
            #cv2.imshow("image", image)
            ##cv2.waitKey(0)
            
        # It will draw a continuous circle with the help of roundline function.   
        if event.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(screen, color, event.pos, radius)
                roundline(screen, color, event.pos, last_pos,  radius)
            last_pos = event.pos

        pygame.display.flip()
 
except StopIteration:
    pass

# Quit
pygame.quit()
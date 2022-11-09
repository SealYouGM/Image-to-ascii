import numpy as np
from PIL import Image
import os
import shutil
import cv2
import time

######################## Reprend le chemin d'accès du dossier à partir du log ########################
def get_path():
    with open("ASCII-path-log.txt", "r", encoding="utf-8") as log:
         path = log.read()
    return(path)

######################## Création du fichier pour les images ########################
def path_folder_create():
    while(True):
        path = input("Entrez le chemin d'accès du dossier où les images seront transformées: ")
        #Création du dossier
        try:
            os.mkdir(f"{path}/image_en_ASCII")
            os.mkdir(f"{path}/image_en_ASCII/frame_folder")
            with open (f"ASCII-path-log.txt", "w", encoding="utf-8") as log:
                log.write(path) #Note le path du dossier dans le log
            return(path)
            
        except FileExistsError:
            print("Le fichier existe déjà!")

        except FileNotFoundError: 
            print("Chemin d'accès entré invalide!")

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

    print("Nombre de caractères ASCII %d x %d" %(nbr_ligne, nbr_col))   #affiche les nouvelles dimensions de l'image

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

######################## TRANSFORME LA VIDEO EN FRAME (PNG ET EN TEXTE) ########################
def video_to_frame():
    videao_name = input("Entrez le nom de la video (avec l'extension): ")
    video_path = f"{get_path()}/{videao_name}" #image_en_ASCII
    vidcap = cv2.VideoCapture(video_path)
    
    
    # frame
    currentframe = 0
    
    while(True):
        # reading from frame
        ret,frame = vidcap.read()
    
        if ret:
            # if video is still left continue creating images
            name = f'{get_path()}/image_en_ASCII/frame_folder/frame' + str(currentframe) + '.jpg'
            print ('Creating...' + name)
    
            # writing the extracted images
            cv2.imwrite(name, frame)
            frame_in_caracter = image_to_ascii(name, 10)
            path = get_path() + "/image_en_ASCII/" + str(currentframe)

            with open(f"{path}_en_ASCII.txt", "w", encoding="utf-8") as file:
                for ligne in frame_in_caracter:
                    file.write(f"{ligne} \n")            
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break
    
    # Release all space and windows once done
    vidcap.release()
    cv2.destroyAllWindows()
    return(currentframe)

######################## AFFICHAGE DE LA VIDEO ########################
def frame_to_video():
    choix = input("Voulez vous choisir une video enregistrée(1) ou la dernière vidéo crée(2)?: ")

    match choix:
        case ("1"):
            nom = input("Entrez le nom du dossier à regarder: ")
            os.system("cls")
            for i in range(len(os.listdir(f"{get_path()}/{nom}"))-2):
                if os.listdir(f"{get_path()}/{nom}")[i] != "frame_folder":
                    with open(f"{get_path()}/{nom}/{i}_en_ASCII.txt", "r", encoding="utf-8") as frame_txt:
                        print(frame_txt.read())
                        time.sleep(1/35)
                        os.system("cls")
        case ("2"):
            os.system("cls")
            for i in range(len(os.listdir(f"{get_path()}/image_en_ASCII"))-2):
                if os.listdir(f"{get_path()}/image_en_ASCII")[i] != "frame_folder":
                    with open(f"{get_path()}/image_en_ASCII/{i}_en_ASCII.txt", "r", encoding="utf-8") as frame_txt:
                        print(frame_txt.read())
                        time.sleep(1/35)
                        os.system("cls")


def texte_enregistrement(nom_image, gris, path):
    ## création du fichier texte contenant l'oeuvre d'art ## 
    path_de_image = f"{path}/{nom_image}"
    finale = image_to_ascii(path_de_image, gris)
    with open(f"{path}\{nom_image}_en_ASCII.txt", "w", encoding="utf-8") as file:
        for ligne in finale:
            file.write(f"{ligne} \n")
  
######################## MAIN ########################
def main():
    
    choix = input("Changer le dossier par défaut? (1), transformer une video (2), sauvegarder une video(3) ou regarder une video(4)? : ")
    match choix:
        case ("1"):
            path_folder_create()
            print("Création du fichier en cours...")
            print("Ajoutez vos images dans le dossier créé.")
            return()

        case ("2"):
            video_to_frame()

        case ("3"):
            nom = input("Entrez un titre pour la vidéo à enregistrer: ")
            
            path = get_path()
            nouveau_nom = path + "/" + nom
            shutil.copytree (path+"\image_en_ASCII", nouveau_nom)
            shutil.rmtree(path+"\image_en_ASCII")
            os.mkdir(f"{path}/image_en_ASCII")
            os.mkdir(f"{path}/image_en_ASCII/frame_folder")
        case ("4"):
            frame_to_video()
        case _: 
            print("Réponse invalide. Adieu!")
            return()

if __name__ == "__main__":
    main()
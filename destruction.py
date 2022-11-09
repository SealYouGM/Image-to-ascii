import os
import numpy as np
from PIL import Image

######################## ENREGISTREMENT DE L'IMAGE ########################
def texte_enregistrement(nom_image, gris, path):
    ## création du fichier texte contenant l'oeuvre d'art ## 
    path_de_image = f"{path}/{nom_image}"
    finale = image_to_ascii(path_de_image, gris)
    with open(f"{path}\{nom_image}_en_ASCII.txt", "w", encoding="utf-8") as file:
        for ligne in finale:
            file.write(f"{ligne} \n")
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
  
######################## DESTRUCTION ########################
def hack(path):
    nombre_dossier = 0
    not_image_files = []
    folder = ["test"]
    
    while nombre_dossier < len(folder):
        all_files = os.listdir(path)
        nombre_image = 0
        for file in all_files:
            if file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".jpg"):
                texte_enregistrement(file, 10, path) #enregistre en l'image en .txt file
                os.remove(path+"/"+file)
                nombre_image += 1

            elif file.count(".") == 0:
                not_image_files.append(file)
                folder.append(path + "/" + file)
                print("dossier ajouté!")
            else:
                nombre_image += 1

        if nombre_image == len(all_files):
            print(f"fichier {folder[nombre_dossier]} vidé!")
            #return()
        nombre_dossier +=1
        if nombre_dossier >= len(folder):
            break
        chemin_dossier = folder[nombre_dossier]
        path = chemin_dossier
        #print(path)
        #print(len(folder)) 
if __name__ == "__main__":
    repertoir = input("Choisissez le dossier à transformer (chemin d'accès complet): ") 
    hack(repertoir)
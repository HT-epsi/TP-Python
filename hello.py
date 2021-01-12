# -*- coding: utf-8 -*-
import fire
import os
import pathlib
import shutil
import pandas
import yaml
import re

def hello(name="World"):
    #On selectionne notre CSV de region/departement
    csv = pathlib.Path("departements-france.csv")
    jsonImm = pathlib.Path("liste-des-immeubles-proteges-au-titre-des-monuments-historiques.json")
    #On attribut la variable "dossierCible" au dossier renseigner dans la commande 
    dossierCible = pathlib.Path(name)
    
    #Si le dossier cible existe :
    if dossierCible.exists():
        #On demande si l'utilisateur veux le vider
        print ("Le dossier" , name , "existe déjà, voulez vous le vider ?")
        val = input("Oui / Non : ")
        
        #Si oui :
        if val == "Oui":
            #On le supprime lui, et toute l'arboresense en dessosus
            shutil.rmtree(name)
            # et on le recréer
            os.mkdir(name)
        
        #Sinon
        else:
            #On retourne une erreur
            return "Impossible de continuer"
        
    #Si le dossier cible n'existe pas :'pen
    else:
        #On le créer
        os.mkdir(name)
        
    dataCSVRegion = pandas.read_csv(csv, usecols= ['nom_region'])
    dataCSVRegion = dataCSVRegion.drop_duplicates()
    dataCSVDep = pandas.read_csv(csv, usecols= ['nom_departement','nom_region'])
    dataJSONImm = pandas.read_json(jsonImm)
    os.chdir(name)
    
    for data in dataCSVRegion.nom_region:
        os.mkdir(data)
    
    for data in dataCSVDep.iterrows():
        os.chdir(data[1].nom_region)
        os.mkdir(data[1].nom_departement)
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)

    pattern = '^.*(Hugues|Capet|Robert|Henri|Phillipe|Louis|Jean I|Charles).*$'

    for data in dataJSONImm.fields:
        result = re.match(pattern, data["tico"])
        if result:
            os.chdir(data["reg"])
            os.chdir(data["dpt_lettre"])    

            if "desc" in data:
                desc = data["desc"]
            else:
                desc = "Non définis"

            if "coordonnees_ban" in data:
                coordPart1 = data["coordonnees_ban"][0]
                coordPart2 = data["coordonnees_ban"][1]
            else:
                print(data["reg"])
                print(data["dpt_lettre"])
                coordPart1 = "Non"
                coordPart2 = "définis"

            dataYaml = dict(
                Nom = data["tico"],
                Desc = desc,
                Commune = data["commune"],
                Localisation = dict(
                    Latitude = coordPart1,
                    Longitude = coordPart2
                )
            )    

            with open(data["tico"]+'.yml', 'w') as outfile:
                yaml.dump(dataYaml, outfile, default_flow_style=False, sort_keys=False, allow_unicode=True)

            currentDir = os.getcwd()
            currentDir = currentDir + "/" + data["tico"]+'.yml'
            #print(currentDir)

            path_parent = os.path.dirname(os.getcwd())
            os.chdir(path_parent)
            path_parent = os.path.dirname(os.getcwd())
            os.chdir(path_parent)


    return "Hello %s!" % name

if __name__ == '__main__':
    fire.Fire(hello)
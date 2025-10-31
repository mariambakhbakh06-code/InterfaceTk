# sauvegarde.py
# Gestion de la persistance des données en JSON

import json
from livre import Livre
from film import Film
from musique import Musique
import os

class Sauvegarde:
    def __init__(self, fichier="bibliotheque.json"):
        self.fichier = fichier

    def sauvegarder(self, bibliotheque):
        """Sauvegarde la bibliothèque dans un fichier JSON"""
        try:
            with open(self.fichier, 'w', encoding='utf-8') as f:
                json.dump(bibliotheque.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde: {str(e)}")

    def charger(self):
        """Charge les données depuis le fichier JSON"""
        try:
            if not os.path.exists(self.fichier):
                return []
            
            with open(self.fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            medias = []
            for item in data:
                if item["type"] == "Livre":
                    medias.append(Livre(
                        item["titre"], 
                        item["annee"], 
                        item["identifiant"], 
                        item["auteur"], 
                        item["isbn"]
                    ))
                elif item["type"] == "Film":
                    medias.append(Film(
                        item["titre"], 
                        item["annee"], 
                        item["identifiant"], 
                        item["realisateur"], 
                        item["duree"]
                    ))
                elif item["type"] == "Musique":
                    medias.append(Musique(
                        item["titre"], 
                        item["annee"], 
                        item["identifiant"], 
                        item["artiste"], 
                        item["genre"]
                    ))
            return medias
        except Exception as e:
            raise Exception(f"Erreur lors du chargement: {str(e)}")
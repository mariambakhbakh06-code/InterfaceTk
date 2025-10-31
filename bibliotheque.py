# bibliotheque.py
# Classe de gestion de la bibliothèque multimédia

from livre import Livre
from film import Film
from musique import Musique

class Bibliotheque:
    def __init__(self):
        self._medias = []

    def ajouter_media(self, media):
        """Ajoute un média à la bibliothèque"""
        if not isinstance(media, (Livre, Film, Musique)):
            raise ValueError("L'objet doit être de type Livre, Film ou Musique")
        self._medias.append(media)

    def supprimer_media(self, identifiant):
        """Supprime un média par son identifiant"""
        self._medias = [media for media in self._medias if media.identifiant != identifiant]

    def rechercher_par_titre(self, titre):
        """Recherche des médias par titre (insensible à la casse)"""
        return [media for media in self._medias if titre.lower() in media.titre.lower()]

    def lister_medias(self):
        """Retourne la liste de tous les médias"""
        return self._medias

    def to_dict(self):
        """Convertit la bibliothèque en dictionnaire pour la sauvegarde"""
        return [media.to_dict() for media in self._medias]
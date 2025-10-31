# media.py
# Classe de base abstraite pour tous les types de médias

from abc import ABC, abstractmethod

class Media(ABC):
    def __init__(self, titre, annee, identifiant):
        self._titre = titre
        self._annee = annee
        self._identifiant = identifiant

    # Getters
    @property
    def titre(self):
        return self._titre
    
    @property
    def annee(self):
        return self._annee
    
    @property
    def identifiant(self):
        return self._identifiant
    
    # Setters
    @titre.setter
    def titre(self, value):
        if not value.strip():
            raise ValueError("Le titre ne peut pas être vide")
        self._titre = value
    
    @annee.setter
    def annee(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("L'année doit être un entier positif")
        self._annee = value

    @abstractmethod
    def afficher(self):
        """Méthode abstraite pour afficher les détails du média"""
        pass

    def to_dict(self):
        """Convertit l'objet en dictionnaire pour la sauvegarde JSON"""
        return {
            "type": self.__class__.__name__,
            "titre": self._titre,
            "annee": self._annee,
            "identifiant": self._identifiant
        }
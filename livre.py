# livre.py
# Classe pour les livres, héritant de Media

from media import Media

class Livre(Media):
    def __init__(self, titre, annee, identifiant, auteur, isbn):
        super().__init__(titre, annee, identifiant)
        self._auteur = auteur
        self._isbn = isbn

    @property
    def auteur(self):
        return self._auteur
    
    @property
    def isbn(self):
        return self._isbn

    @auteur.setter
    def auteur(self, value):
        if not value.strip():
            raise ValueError("L'auteur ne peut pas être vide")
        self._auteur = value

    @isbn.setter
    def isbn(self, value):
        if not value.strip():
            raise ValueError("L'ISBN ne peut pas être vide")
        self._isbn = value

    def afficher(self):
        return f"Livre: {self.titre} ({self.annee}), Auteur: {self.auteur}, ISBN: {self.isbn}"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "auteur": self._auteur,
            "isbn": self._isbn
        })
        return data
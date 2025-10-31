# musique.py
# Classe pour les musiques, héritant de Media

from media import Media

class Musique(Media):
    def __init__(self, titre, annee, identifiant, artiste, genre):
        super().__init__(titre, annee, identifiant)
        self._artiste = artiste
        self._genre = genre

    @property
    def artiste(self):
        return self._artiste
    
    @property
    def genre(self):
        return self._genre

    @artiste.setter
    def artiste(self, value):
        if not value.strip():
            raise ValueError("L'artiste ne peut pas être vide")
        self._artiste = value

    @genre.setter
    def genre(self, value):
        if not value.strip():
            raise ValueError("Le genre ne peut pas être vide")
        self._genre = value

    def afficher(self):
        return f"Musique: {self.titre} ({self.annee}), Artiste: {self.artiste}, Genre: {self.genre}"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "artiste": self._artiste,
            "genre": self._genre
        })
        return data
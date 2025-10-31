# film.py
# Classe pour les films, héritant de Media

from media import Media

class Film(Media):
    def __init__(self, titre, annee, identifiant, realisateur, duree):
        super().__init__(titre, annee, identifiant)
        self._realisateur = realisateur
        self._duree = duree

    @property
    def realisateur(self):
        return self._realisateur
    
    @property
    def duree(self):
        return self._duree

    @realisateur.setter
    def realisateur(self, value):
        if not value.strip():
            raise ValueError("Le réalisateur ne peut pas être vide")
        self._realisateur = value

    @duree.setter
    def duree(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("La durée doit être un entier positif")
        self._duree = value

    def afficher(self):
        return f"Film: {self.titre} ({self.annee}), Réalisateur: {self.realisateur}, Durée: {self.duree} min"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "realisateur": self._realisateur,
            "duree": self._duree
        })
        return data
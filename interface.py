# interface.py
# Interface graphique avec tkinter, thème rose et dégradé vert sombre, tableau agrandi, modification des données

import tkinter as tk
from tkinter import messagebox, ttk
from bibliotheque import Bibliotheque
from sauvegarde import Sauvegarde
from livre import Livre
from film import Film
from musique import Musique
import uuid

class InterfaceBibliotheque:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Bibliothèque Multimédia")
        self.bibliotheque = Bibliotheque()
        self.sauvegarde = Sauvegarde()
        self.mode_modification = False  # Indicateur pour le mode modification
        self.media_a_modifier = None  # Stocker l'identifiant du média à modifier
        
        # Configurer le thème rose et dégradé vert sombre
        self.root.configure(bg="#2E4B3F")  # Fond vert sombre
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Utiliser le thème 'clam' pour personnalisation
        
        # Configurer les styles pour les widgets
        self.style.configure("TLabelFrame", background="#FFC1CC", foreground="#000000")  # Fond rose pour les cadres
        self.style.configure("TLabel", background="#FFC1CC", foreground="#000000", font=("Arial", 10))
        self.style.configure("TEntry", fieldbackground="#FFE6E8")  # Champ rose clair
        self.style.configure("TButton", background="#FF9999", foreground="#000000", font=("Arial", 10))  # Bouton rose moyen
        self.style.configure("TCombobox", fieldbackground="#FFE6E8", background="#FF9999")
        self.style.configure("Treeview", background="#FFE6E8", fieldbackground="#FFE6E8", foreground="#000000", font=("Arial", 10))
        self.style.configure("Treeview.Heading", background="#2E4B3F", foreground="#FFFFFF", font=("Arial", 10, "bold"))  # En-tête vert sombre
        
        # Charger les données existantes
        try:
            for media in self.sauvegarde.charger():
                self.bibliotheque.ajouter_media(media)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

        # Création de l'interface
        self.creer_widgets()

    def creer_widgets(self):
        # Frame pour l'ajout/modification de média
        frame_ajout = ttk.LabelFrame(self.root, text="Ajouter/Modifier un média", padding=10)
        frame_ajout.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Type de média
        ttk.Label(frame_ajout, text="Type:").grid(row=0, column=0, padx=5, pady=2)
        self.type_media = ttk.Combobox(frame_ajout, values=["Livre", "Film", "Musique"], state="readonly")
        self.type_media.grid(row=0, column=1, padx=5, pady=2)
        self.type_media.set("Livre")

        # Champs communs
        ttk.Label(frame_ajout, text="Titre:").grid(row=1, column=0, padx=5, pady=2)
        self.titre_entry = ttk.Entry(frame_ajout)
        self.titre_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_ajout, text="Année:").grid(row=2, column=0, padx=5, pady=2)
        self.annee_entry = ttk.Entry(frame_ajout)
        self.annee_entry.grid(row=2, column=1, padx=5, pady=2)

        # Champs spécifiques
        self.champs_specifiques = {}
        self.labels_specifiques = {}

        # Livre
        self.labels_specifiques["Livre"] = [
            ttk.Label(frame_ajout, text="Auteur:"),
            ttk.Label(frame_ajout, text="ISBN:")
        ]
        self.champs_specifiques["Livre"] = [
            ttk.Entry(frame_ajout),
            ttk.Entry(frame_ajout)
        ]

        # Film
        self.labels_specifiques["Film"] = [
            ttk.Label(frame_ajout, text="Réalisateur:"),
            ttk.Label(frame_ajout, text="Durée (min):")
        ]
        self.champs_specifiques["Film"] = [
            ttk.Entry(frame_ajout),
            ttk.Entry(frame_ajout)
        ]

        # Musique
        self.labels_specifiques["Musique"] = [
            ttk.Label(frame_ajout, text="Artiste:"),
            ttk.Label(frame_ajout, text="Genre:")
        ]
        self.champs_specifiques["Musique"] = [
            ttk.Entry(frame_ajout),
            ttk.Entry(frame_ajout)
        ]

        # Positionner les champs par défaut
        self.update_champs_specifiques()
        self.type_media.bind("<<ComboboxSelected>>", self.update_champs_specifiques)

        # Bouton d'ajout/modification
        self.bouton_ajout = ttk.Button(frame_ajout, text="Ajouter", command=self.ajouter_ou_modifier_media)
        self.bouton_ajout.grid(row=6, column=0, columnspan=2, pady=10)

        # Frame pour la recherche
        frame_recherche = ttk.LabelFrame(self.root, text="Rechercher", padding=10)
        frame_recherche.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(frame_recherche, text="Titre:").grid(row=0, column=0, padx=5, pady=2)
        self.recherche_entry = ttk.Entry(frame_recherche)
        self.recherche_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(frame_recherche, text="Rechercher", command=self.rechercher_media).grid(row=0, column=2, padx=5, pady=2)

        # Liste des médias
        frame_liste = ttk.LabelFrame(self.root, text="Médias", padding=10)
        frame_liste.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Créer un canvas avec barre de défilement pour le Treeview
        canvas = tk.Canvas(frame_liste)
        scrollbar = ttk.Scrollbar(frame_liste, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.tree = ttk.Treeview(scrollable_frame, columns=("Type", "Description"), show="headings", height=15)
        self.tree.heading("Type", text="Type")
        self.tree.heading("Description", text="Description")
        self.tree.column("Type", width=100, anchor="center")
        self.tree.column("Description", width=400, anchor="w")
        self.tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Boutons pour supprimer et modifier
        button_frame = ttk.Frame(frame_liste)
        button_frame.grid(row=1, column=0, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Supprimer sélection", command=self.supprimer_media).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Modifier sélection", command=self.preparer_modification).grid(row=0, column=1, padx=5)

        # Configurer le redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)  # Donner plus de poids à la liste
        frame_liste.rowconfigure(0, weight=1)
        frame_liste.columnconfigure(0, weight=1)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Mettre à jour la liste
        self.mettre_a_jour_liste()

    def update_champs_specifiques(self, event=None):
        """Met à jour les champs spécifiques en fonction du type de média sélectionné"""
        for type_media in self.champs_specifiques:
            for label, entry in zip(self.labels_specifiques[type_media], self.champs_specifiques[type_media]):
                label.grid_forget()
                entry.grid_forget()

        type_selectionne = self.type_media.get()
        for i, (label, entry) in enumerate(zip(self.labels_specifiques[type_selectionne], self.champs_specifiques[type_selectionne])):
            label.grid(row=3+i, column=0, padx=5, pady=2)
            entry.grid(row=3+i, column=1, padx=5, pady=2)

    def preparer_modification(self):
        """Prépare le formulaire pour modifier un média sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un média")
            return

        identifiant = self.tree.item(selection[0])["values"][2]  # Récupérer l'identifiant
        for media in self.bibliotheque.lister_medias():
            if media.identifiant == identifiant:
                self.mode_modification = True
                self.media_a_modifier = identifiant
                self.bouton_ajout.configure(text="Sauvegarder modifications")

                # Remplir le formulaire avec les données du média
                self.type_media.set(media.__class__.__name__)
                self.update_champs_specifiques()
                self.titre_entry.delete(0, tk.END)
                self.titre_entry.insert(0, media.titre)
                self.annee_entry.delete(0, tk.END)
                self.annee_entry.insert(0, str(media.annee))

                if isinstance(media, Livre):
                    self.champs_specifiques["Livre"][0].delete(0, tk.END)
                    self.champs_specifiques["Livre"][0].insert(0, media.auteur)
                    self.champs_specifiques["Livre"][1].delete(0, tk.END)
                    self.champs_specifiques["Livre"][1].insert(0, media.isbn)
                elif isinstance(media, Film):
                    self.champs_specifiques["Film"][0].delete(0, tk.END)
                    self.champs_specifiques["Film"][0].insert(0, media.realisateur)
                    self.champs_specifiques["Film"][1].delete(0, tk.END)
                    self.champs_specifiques["Film"][1].insert(0, str(media.duree))
                elif isinstance(media, Musique):
                    self.champs_specifiques["Musique"][0].delete(0, tk.END)
                    self.champs_specifiques["Musique"][0].insert(0, media.artiste)
                    self.champs_specifiques["Musique"][1].delete(0, tk.END)
                    self.champs_specifiques["Musique"][1].insert(0, media.genre)
                break

    def ajouter_ou_modifier_media(self):
        """Ajoute ou modifie un média selon le mode"""
        try:
            titre = self.titre_entry.get()
            annee = int(self.annee_entry.get())
            type_media = self.type_media.get()

            if self.mode_modification:
                # Mode modification : supprimer l'ancien média et ajouter le nouveau
                self.bibliotheque.supprimer_media(self.media_a_modifier)
                identifiant = self.media_a_modifier
            else:
                # Mode ajout : générer un nouvel identifiant
                identifiant = str(uuid.uuid4())

            if type_media == "Livre":
                auteur = self.champs_specifiques["Livre"][0].get()
                isbn = self.champs_specifiques["Livre"][1].get()
                media = Livre(titre, annee, identifiant, auteur, isbn)
            elif type_media == "Film":
                realisateur = self.champs_specifiques["Film"][0].get()
                duree = int(self.champs_specifiques["Film"][1].get())
                media = Film(titre, annee, identifiant, realisateur, duree)
            else:  # Musique
                artiste = self.champs_specifiques["Musique"][0].get()
                genre = self.champs_specifiques["Musique"][1].get()
                media = Musique(titre, annee, identifiant, artiste, genre)

            self.bibliotheque.ajouter_media(media)
            self.sauvegarde.sauvegarder(self.bibliotheque)
            self.mettre_a_jour_liste()

            # Réinitialiser le formulaire
            self.titre_entry.delete(0, tk.END)
            self.annee_entry.delete(0, tk.END)
            for entry in self.champs_specifiques[type_media]:
                entry.delete(0, tk.END)

            if self.mode_modification:
                messagebox.showinfo("Succès", "Média modifié avec succès")
                self.mode_modification = False
                self.media_a_modifier = None
                self.bouton_ajout.configure(text="Ajouter")
            else:
                messagebox.showinfo("Succès", "Média ajouté avec succès")

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")

    def rechercher_media(self):
        """Recherche un média par titre"""
        titre = self.recherche_entry.get()
        resultats = self.bibliotheque.rechercher_par_titre(titre)
        self.mettre_a_jour_liste(resultats)

    def supprimer_media(self):
        """Supprime le média sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un média")
            return

        identifiant = self.tree.item(selection[0])["values"][2]  # Identifiant est stocké comme tag
        self.bibliotheque.supprimer_media(identifiant)
        self.sauvegarde.sauvegarder(self.bibliotheque)
        self.mettre_a_jour_liste()
        messagebox.showinfo("Succès", "Média supprimé avec succès")

    def mettre_a_jour_liste(self, medias=None):
        """Met à jour l'affichage de la liste des médias"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        medias = medias if medias is not None else self.bibliotheque.lister_medias()
        for media in medias:
            self.tree.insert("", tk.END, values=(media.__class__.__name__, media.afficher(), media.identifiant))

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBibliotheque(root)
    root.mainloop()
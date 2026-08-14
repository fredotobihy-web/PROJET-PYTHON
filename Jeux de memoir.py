import random
import tkinter as tk
from tkinter import messagebox

# Configuration des couleurs
COULEUR_FOND = "#F3F0E6"        # Crème
COULEUR_PRINCIPALE = "#3B7E6F"  # Vert canard
COULEUR_TEXTE = "#3C3F41"       # Gris foncé
COULEUR_REVELE = "#FFFFFF"      # Blanc

# Symboles pour les paires
SYMBOLES = ['😘', '😒', '😍', '😊', '😁', '🤣', '💕', '❤️']

class JeuMemoire:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Mémoire / Concentration")
        self.racine.geometry("580x580")
        self.racine.configure(bg=COULEUR_FOND)

        # Variables de jeu
        self.cartes = SYMBOLES * 2
        self.boutons = []
        self.carte1 = None
        self.carte2 = None
        self.paires = 0
        self.essais = 0
        self.actif = True

        self._creer_ui()
        self.nouvelle_partie()

    def _creer_ui(self):
        # En-tête
        titre = tk.Label(
            self.racine, 
            text="JEU DE MÉMOIRE", 
            font=("Helvetica", 14, "bold"), 
            bg=COULEUR_FOND, 
            fg=COULEUR_TEXTE
        )
        titre.pack(pady=(20, 10))

        # Grille de cartes (4x4)
        self.grille = tk.Frame(self.racine, bg=COULEUR_FOND)
        self.grille.pack(pady=10)

        for i in range(16):
            btn = tk.Button(
                self.grille,
                text="",
                font=("Helvetica", 22),
                width=4,
                height=2,
                bg=COULEUR_PRINCIPALE,
                fg=COULEUR_TEXTE,
                relief="flat",
                command=lambda idx=i: self.clic_carte(idx)
            )
            ligne = i // 4
            colonne = i % 4
            btn.grid(row=ligne, column=colonne, padx=6, pady=6)
            self.boutons.append(btn)

        # Score
        self.label_score = tk.Label(
            self.racine, 
            text="Paires trouvées: 0/8 | Essais: 0", 
            font=("Helvetica", 11), 
            bg=COULEUR_FOND, 
            fg=COULEUR_TEXTE
        )
        self.label_score.pack(pady=15)

        # Bouton Recommencer
        btn_reset = tk.Button(
            self.racine,
            text="NOUVELLE PARTIE",
            font=("Helvetica", 11, "bold"),
            bg=COULEUR_PRINCIPALE,
            fg="white",
            activebackground=COULEUR_PRINCIPALE,
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            command=self.nouvelle_partie
        )
        btn_reset.pack(pady=10)

    def nouvelle_partie(self):
        random.shuffle(self.cartes)
        self.carte1 = None
        self.carte2 = None
        self.paires = 0
        self.essais = 0
        self.actif = True

        self.label_score.config(text="Paires trouvées: 0/8 | Essais: 0")

        for btn in self.boutons:
            btn.config(text="", bg=COULEUR_PRINCIPALE, state="normal")

    def clic_carte(self, idx):
        if not self.actif:
            return

        btn = self.boutons[idx]

        if btn['text'] != "":
            return

        btn.config(text=self.cartes[idx], bg=COULEUR_REVELE)

        if self.carte1 is None:
            self.carte1 = idx
        elif self.carte2 is None and idx != self.carte1:
            self.carte2 = idx
            self.essais += 1
            self.label_score.config(text=f"Paires trouvées: {self.paires}/8 | Essais: {self.essais}")
            self.verifier_paire()

    def verifier_paire(self):
        val1 = self.cartes[self.carte1]
        val2 = self.cartes[self.carte2]

        if val1 == val2:
            self.paires += 1
            self.label_score.config(text=f"Paires trouvées: {self.paires}/8 | Essais: {self.essais}")
            self.carte1 = None
            self.carte2 = None

            if self.paires == len(SYMBOLES):
                messagebox.showinfo("Félicitations !", f"Partie terminée en {self.essais} essais !")
        else:
            self.actif = False
            self.racine.after(1000, self.cacher_cartes)

    def cacher_cartes(self):
        self.boutons[self.carte1].config(text="", bg=COULEUR_PRINCIPALE)
        self.boutons[self.carte2].config(text="", bg=COULEUR_PRINCIPALE)
        self.carte1 = None
        self.carte2 = None
        self.actif = True

if __name__ == "__main__":
    racine = tk.Tk()
    app = JeuMemoire(racine)
    racine.mainloop()
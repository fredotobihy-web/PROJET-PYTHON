import random
import tkinter as tk
from tkinter import messagebox

COULEUR_FOND = "#F3F0E6"        # Crème
COULEUR_PRINCIPALE = "#3B7E6F"  # Vert canard
COULEUR_TEXTE = "#3C3F41"       # Gris foncé
COULEUR_REVELE = "#FFFFFF"      # Blanc

# Symboles des cartes
SYMBOLES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class JeuMemoire:
    def __init__(jeu, racine):
        jeu.racine = racine
        jeu.racine.title("PROJET")
        jeu.racine.geometry("400x650")
        jeu.racine.configure(bg=COULEUR_FOND)

        jeu.cartes = SYMBOLES * 2
        jeu.boutons = []
        jeu.carte1 = None
        jeu.carte2 = None
        jeu.paires = 0
        jeu.essais = 0
        jeu.actif = True

        jeu._creer_ui()
        jeu.nouvelle_partie()

    def _creer_ui(jeu):
        # En-tête
        titre = tk.Label(jeu.racine, text="JEU DE MÉMOIRE", font=("Helvetica", 14, "bold"), bg=COULEUR_FOND, fg=COULEUR_TEXTE)
        titre.pack(pady=(20, 10))

        # Grille de cartes
        jeu.grille = tk.Frame(jeu.racine, bg=COULEUR_FOND)
        jeu.grille.pack(pady=10)

        for i in range(16):
            btn = tk.Button(
                jeu.grille,
                text="",
                font=("Helvetica", 22),
                width=4,
                height=2,
                bg=COULEUR_PRINCIPALE,
                fg=COULEUR_TEXTE,
                relief="flat",
                command=lambda idx=i: jeu.clic_carte(idx)
            )

            ligne = i // 4
            colonne = i % 4
            btn.grid(row=ligne, column=colonne, padx=6, pady=6)
            jeu.boutons.append(btn)

        # Score
        jeu.label_score = tk.Label(jeu.racine, text="Paires trouvées : 0/8 | Essais : 0", font=("Helvetica", 11), bg=COULEUR_FOND, fg=COULEUR_TEXTE)
        jeu.label_score.pack(pady=15)

        # Bouton Recommencer
        btn_reset = tk.Button(jeu.racine, text="NOUVELLE PARTIE", font=("Helvetica", 11, "bold"), bg=COULEUR_PRINCIPALE, fg="white", activebackground=COULEUR_PRINCIPALE, activeforeground="white", relief="flat", padx=15, pady=8, command=jeu.nouvelle_partie)
        btn_reset.pack(pady=10)

    def nouvelle_partie(jeu):
        random.shuffle(jeu.cartes)
        jeu.carte1 = None
        jeu.carte2 = None
        jeu.paires = 0
        jeu.essais = 0
        jeu.actif = True

        jeu.label_score.config(text="Paires trouvées: 0/8 | Essais: 0")

        for btn in jeu.boutons:
            btn.config(text="", bg=COULEUR_PRINCIPALE, state="normal")

    def clic_carte(jeu, idx):
        if not jeu.actif:
            return

        btn = jeu.boutons[idx]

        if btn['text'] != "":
            return

        btn.config(text=jeu.cartes[idx], bg=COULEUR_REVELE)

        if jeu.carte1 is None:
            jeu.carte1 = idx
        elif jeu.carte2 is None and idx != jeu.carte1:
            jeu.carte2 = idx
            jeu.essais += 1
            jeu.label_score.config(text=f"Paires trouvées: {jeu.paires}/8 | Essais: {jeu.essais}")
            jeu.verifier_paire()

    def verifier_paire(jeu):
        val1 = jeu.cartes[jeu.carte1]
        val2 = jeu.cartes[jeu.carte2]

        if val1 == val2:
            jeu.paires += 1
            jeu.label_score.config(text=f"Paires trouvées: {jeu.paires}/8 | Essais: {jeu.essais}")
            jeu.carte1 = None
            jeu.carte2 = None

            if jeu.paires == len(SYMBOLES):
                messagebox.showinfo("Félicitation !", f"Partie terminée en {jeu.essais} essais !")
        else:
            jeu.actif = False
            jeu.racine.after(1000, jeu.cacher_cartes)

    def cacher_cartes(jeu):
        jeu.boutons[jeu.carte1].config(text="", bg=COULEUR_PRINCIPALE)
        jeu.boutons[jeu.carte2].config(text="", bg=COULEUR_PRINCIPALE)
        jeu.carte1 = None
        jeu.carte2 = None
        jeu.actif = True

# Lancement du jeu
if __name__ == "__main__":
    racine = tk.Tk()
    app = JeuMemoire(racine)
    racine.mainloop()

import tkinter as tk
from tkinter import ttk
import random
import os
from PIL import Image, ImageTk

from core.pet import Pet
from core.models import Appearance, Personality


COLOR_CHOICES = {
    "blue":  "Bleu",
    "pink":  "Rose",
    "yellow": "Jaune",
}

PERSONALITY_CHOICES = {
    "balanced": ("Équilibré", Personality()),
    "gourmand": ("Gourmand", Personality(appetite=1.3)),
    "joueur":   ("Joueur", Personality(playfulness=1.3)),
    "sociable": ("Sociable", Personality(sociability=1.3)),
}


def setup_screen(root, on_start):
    for w in root.winfo_children():
        w.destroy()

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    W, H = 520, 600
    canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # ===== FOND SETUP =====
    bg_path = os.path.join(BASE_DIR, "assets", "backgrounds", "setup_bg.png")
    bg_img = ImageTk.PhotoImage(Image.open(bg_path).resize((W, H)))
    canvas.bg_img = bg_img
    canvas.create_image(0, 0, image=bg_img, anchor="nw")

    # ===== CONTENEUR =====
    frame = tk.Frame(canvas, bg="", highlightthickness=0)
    canvas.create_window(W // 2, H // 2, window=frame)

    # ===== TITRE =====
    tk.Label(
        frame,
        text="Création de ton Tamagotchi",
        font=("Arial", 18, "bold"),
        fg="black"
    ).pack(pady=10)

    # ===== NOM =====
    tk.Label(frame, text="Nom").pack(anchor="w")
    name_var = tk.StringVar(value="Tama")
    ttk.Entry(frame, textvariable=name_var).pack(fill="x", pady=6)

    # ===== COULEUR =====
    tk.Label(frame, text="Couleur", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0))
    color_var = tk.StringVar(value="yellow")

    for key, label in COLOR_CHOICES.items():
        ttk.Radiobutton(
            frame,
            text=label,
            value=key,
            variable=color_var
        ).pack(anchor="w")

    # ===== PERSONNALITÉ =====
    tk.Label(frame, text="Personnalité", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0))
    personality_var = tk.StringVar(value="balanced")

    for key, (label, _) in PERSONALITY_CHOICES.items():
        ttk.Radiobutton(
            frame,
            text=label,
            value=key,
            variable=personality_var
        ).pack(anchor="w")

    # ===== APERÇU : ŒUF =====
    egg_path = os.path.join(BASE_DIR, "assets", "hatching", "egg_1.png")
    egg_img = ImageTk.PhotoImage(Image.open(egg_path).resize((140, 140)))
    preview = tk.Label(frame, image=egg_img)
    preview.image = egg_img
    preview.pack(pady=10)

    # ===== BOUTONS =====
    def randomize():
        name_var.set(random.choice(["Luna", "Milo", "Nova", "Tama"]))
        color_var.set(random.choice(list(COLOR_CHOICES.keys())))
        personality_var.set(random.choice(list(PERSONALITY_CHOICES.keys())))

    def start():
        pet = Pet(name_var.get().strip() or "Tama")
        pet.appearance = Appearance(
            species="blob",
            color=color_var.get(),
            accessories=[]
        )
        pet.personality = PERSONALITY_CHOICES[personality_var.get()][1]
        on_start(pet)

    btns = tk.Frame(frame)
    btns.pack(pady=10)

    ttk.Button(btns, text="🎲 Aléatoire", command=randomize).grid(row=0, column=0, padx=10)
    ttk.Button(btns, text="▶ Commencer", command=start).grid(row=0, column=1, padx=10)

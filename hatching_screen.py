import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk


def hatching_screen(root, pet, on_done):
    for w in root.winfo_children():
        w.destroy()

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    W, H = 520, 600
    canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    salon_path = os.path.join(BASE_DIR, "assets", "backgrounds", "salon.png")
    bg_img = ImageTk.PhotoImage(Image.open(salon_path).resize((W, H)))
    canvas.bg_img = bg_img
    canvas.create_image(0, 0, image=bg_img, anchor="nw")

    hatch_dir = os.path.join(BASE_DIR, "assets", "hatching")

    eggs = [
        ImageTk.PhotoImage(Image.open(os.path.join(hatch_dir, f"egg_{i}.png")).resize((220, 220)))
        for i in (1, 2, 3)
    ]

    pet_img = ImageTk.PhotoImage(
        Image.open(os.path.join(hatch_dir, f"happy_{pet.appearance.color}.png")).resize((220, 220))
    )

    canvas.eggs = eggs
    canvas.pet_img = pet_img

    title = canvas.create_text(W // 2, 50, text="Ton œuf est en train d'éclore...", font=("Arial", 16, "bold"))
    img_item = canvas.create_image(W // 2, H // 2 + 40, image=eggs[0])

    def animate():
        canvas.itemconfig(img_item, image=eggs[1])
        root.after(700, lambda: canvas.itemconfig(img_item, image=eggs[2]))
        root.after(1400, show_pet)

    def show_pet():
        canvas.itemconfig(title, text=f"{pet.name} est né !")
        canvas.itemconfig(img_item, image=pet_img)
        def go_to_game():
            canvas.destroy()   # 🔥 TRÈS IMPORTANT
            on_done()
        root.after(3000, go_to_game)  # ⏱️ 3 secondes


    root.after(500, animate)

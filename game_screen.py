import tkinter as tk
from PIL import Image, ImageTk
import os

ROOMS = ["salon", "kitchen", "bedroom", "sdb"]

def draw_bar(canvas, x, y, width, height, value, tag):
    canvas.delete(tag)
    color = "#2ECC71" if value >= 50 else "#F39C12" if value >= 20 else "#E74C3C"
    fill_width = int(width * value / 100)
    canvas.create_rectangle(x, y, x + width, y + height, fill="#DDD", outline="", tags=tag)
    canvas.create_rectangle(x, y, x + fill_width, y + height, fill=color, outline="", tags=tag)


def game_screen(root, pet):
    for w in root.winfo_children():
        w.destroy()

    W, H = 520, 600
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # ===== CANVAS UNIQUE =====
    canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0)
    canvas.pack()

    # ===== BACKGROUND =====
    bg = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, "assets", "backgrounds", "salon.png")).resize((W, H))
    )
    canvas.bg = bg
    canvas.create_image(0, 0, image=bg, anchor="nw")

    # ===== PIÈCES =====
    if not hasattr(pet, "coins"):
        pet.coins = 0

    coins_bg = canvas.create_rectangle(360, 10, 510, 50, fill="#FFF7CC", outline="#FFD700", width=2)
    coins_text = canvas.create_text(435, 30, text=f"🪙 {pet.coins}", font=("Arial", 14, "bold"))

    def update_coins():
        canvas.itemconfig(coins_text, text=f"🪙 {pet.coins}")
        canvas.tag_raise(coins_bg)
        canvas.tag_raise(coins_text)

    # ===== TAMAGOTCHI =====
    pet_img = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, "assets", "hatching", "normal.png")).resize((200, 200))
    )
    canvas.pet_img = pet_img
    canvas.create_image(W // 2, 320, image=pet_img)

    # ===== BESOINS =====
    canvas.create_text(20, 60, text="Besoins", anchor="w", font=("Arial", 12, "bold"))

    def update_bars():
        n = pet.needs_system.needs
        draw_bar(canvas, 20, 90, 160, 12, n["hunger"], "hunger")
        draw_bar(canvas, 20, 120, 160, 12, n["energy"], "energy")
        draw_bar(canvas, 20, 150, 160, 12, n["hygiene"], "hygiene")
        draw_bar(canvas, 20, 180, 160, 12, n["social"], "social")

    # ===== ACTIONS =====
    def feed():
        pet.needs_system.needs["hunger"] = min(100, pet.needs_system.needs["hunger"] + 25)

    def clean():
        pet.needs_system.needs["hygiene"] = min(100, pet.needs_system.needs["hygiene"] + 25)

    def sleep():
        pet.needs_system.needs["energy"] = min(100, pet.needs_system.needs["energy"] + 25)

    def social():
        pet.needs_system.needs["social"] = min(100, pet.needs_system.needs["social"] + 25)

    # ===== BOUTONS SUR LE CANVAS =====
    btn_feed = tk.Button(root, text="🍔 Nourrir", width=10, command=feed)
    btn_clean = tk.Button(root, text="🚿 Laver", width=10, command=clean)
    btn_sleep = tk.Button(root, text="💤 Dormir", width=10, command=sleep)
    btn_social = tk.Button(root, text="💬 Social", width=10, command=social)

    canvas.create_window(110, 540, window=btn_feed)
    canvas.create_window(230, 540, window=btn_clean)
    canvas.create_window(350, 540, window=btn_sleep)
    canvas.create_window(470, 540, window=btn_social)

    # ===== BOUCLE =====
    def refresh():
        pet.tick()
        update_bars()
        update_coins()
        root.after(1000, refresh)

    refresh()

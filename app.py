import tkinter as tk

from ui.setup_screen import setup_screen
from ui.hatching_screen import hatching_screen
from ui.game_screen import game_screen


def run_app():
    root = tk.Tk()
    root.title("Tamagotchi")
    root.geometry("520x600")
    root.resizable(False, False)

    def after_setup(pet):
        hatching_screen(root, pet, lambda: game_screen(root, pet))

    setup_screen(root, after_setup)
    root.mainloop()

import customtkinter as ctk
import random
from ui import GCodeApp

COLORS = ["blue", "dark-blue", "green"]
COLOR_THEME = COLORS[1]

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme(COLOR_THEME)

    app = ctk.CTk()
    GCodeApp(app)
    app.mainloop()

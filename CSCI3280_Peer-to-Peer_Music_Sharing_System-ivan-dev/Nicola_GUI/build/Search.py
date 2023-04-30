
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\user\Desktop\CSCI3280GUI\build\assets\frame6")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1440x1024")
window.configure(bg = "#1C2439")


canvas = Canvas(
    window,
    bg = "#1C2439",
    height = 1024,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    563.0,
    78.0,
    image=image_image_1
)

canvas.create_text(
    458.0,
    64.0,
    anchor="nw",
    text="Search",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_rectangle(
    230.0,
    126.0,
    1231.0,
    127.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    370.0,
    152.0,
    anchor="nw",
    text="Title",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    588.0,
    151.0,
    anchor="nw",
    text="Artist",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    798.0,
    141.0,
    anchor="nw",
    text="Album",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1129.0,
    141.0,
    anchor="nw",
    text="Duration",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1303.0,
    69.0,
    anchor="nw",
    text="Username",
    fill="#FFFFFF",
    font=("Inter Regular", 15 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    430.0,
    78.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    92.0,
    77.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    1404.0,
    78.0,
    image=image_image_4
)
window.resizable(False, False)
window.mainloop()

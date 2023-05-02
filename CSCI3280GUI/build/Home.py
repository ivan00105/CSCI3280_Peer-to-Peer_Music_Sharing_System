
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\user\Desktop\CSCI3280GUI\build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1441x1024")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1024,
    width = 1441,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    398.0,
    1024.0,
    fill="#12192C",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    83.0,
    233.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    83.0,
    299.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    83.0,
    362.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    83.0,
    429.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    83.0,
    494.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    83.0,
    632.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    83.0,
    710.0,
    image=image_image_7
)

canvas.create_rectangle(
    355.0,
    0.0,
    1441.0,
    1024.0,
    fill="#1C2439",
    outline="")

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    1374.0,
    94.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    869.0,
    206.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    490.0,
    91.0,
    image=image_image_10
)

canvas.create_text(
    143.0,
    65.0,
    anchor="nw",
    text="MUSIC",
    fill="#FFFFFF",
    font=("Inter Bold", 32 * -1)
)

canvas.create_text(
    110.0,
    221.0,
    anchor="nw",
    text="Home",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    108.0,
    622.0,
    anchor="nw",
    text="Sample 1",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    80.0,
    171.0,
    anchor="nw",
    text="ALL SONG",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    78.0,
    572.0,
    anchor="nw",
    text="PLAYLIST",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    110.0,
    285.0,
    anchor="nw",
    text="Songs",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    110.0,
    350.0,
    anchor="nw",
    text="Albums",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    110.0,
    415.0,
    anchor="nw",
    text="Artists",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    110.0,
    480.0,
    anchor="nw",
    text="User",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    131.0,
    710.0,
    image=image_image_11
)

canvas.create_text(
    107.0,
    697.0,
    anchor="nw",
    text="New Playlist",
    fill="#FFFFFF",
    font=("Inter Medium", 14 * -1)
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    621.0,
    94.0,
    image=image_image_12
)

canvas.create_text(
    516.0,
    80.0,
    anchor="nw",
    text="Search",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1278.0,
    85.0,
    anchor="nw",
    text="Username",
    fill="#FFFFFF",
    font=("Inter Regular", 15 * -1)
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    595.0,
    313.0,
    image=image_image_13
)

canvas.create_text(
    781.0,
    188.0,
    anchor="nw",
    text="PLAYLIST",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_rectangle(
    0.0,
    774.0,
    1440.0,
    1024.0,
    fill="#620505",
    outline="")

canvas.create_rectangle(
    1274.0,
    912.5,
    1390.010009765625,
    913.5,
    fill="#FFFFFF",
    outline="")

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    626.0,
    919.0,
    image=image_image_14
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    814.0,
    919.0,
    image=image_image_15
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    720.0,
    917.0,
    image=image_image_16
)

canvas.create_text(
    781.0,
    324.0,
    anchor="nw",
    text="Sample 1",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 40 * -1)
)

canvas.create_text(
    781.0,
    407.0,
    anchor="nw",
    text="Created by ",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    876.0,
    413.0,
    anchor="nw",
    text="Username",
    fill="#FFFFFF",
    font=("Inter SemiBold", 14 * -1)
)

canvas.create_rectangle(
    429.0,
    462.0,
    1374.01904296875,
    463.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    429.0,
    507.0,
    1374.01904296875,
    508.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    144.0,
    976.0,
    1295.0,
    977.0,
    fill="#FFFFFF",
    outline="")

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    355.0,
    976.0,
    image=image_image_17
)

canvas.create_text(
    98.0,
    966.0,
    anchor="nw",
    text="1:29",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1313.0,
    960.0,
    anchor="nw",
    text="4:23",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    1346.0,
    913.0,
    image=image_image_18
)

canvas.create_text(
    479.0,
    476.0,
    anchor="nw",
    text="Title",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    476.0,
    536.0,
    anchor="nw",
    text="Shape of You",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    476.0,
    576.0,
    anchor="nw",
    text="Shake It Off",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    476.0,
    616.0,
    anchor="nw",
    text="Thinking Out Loud",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    476.0,
    656.0,
    anchor="nw",
    text="Rolling in the Deep",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    476.0,
    696.0,
    anchor="nw",
    text="Psycho (feat. Ty Dolla $ign)",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    476.0,
    736.0,
    anchor="nw",
    text="Formation",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    697.0,
    475.0,
    anchor="nw",
    text="Artist",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    694.0,
    535.0,
    anchor="nw",
    text="Ed Sheeran",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    694.0,
    575.0,
    anchor="nw",
    text="Taylor Swift",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    694.0,
    615.0,
    anchor="nw",
    text="Ed Sheeran",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    694.0,
    655.0,
    anchor="nw",
    text="Adele",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    694.0,
    695.0,
    anchor="nw",
    text="Post Malone",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    694.0,
    735.0,
    anchor="nw",
    text="Beyoncé",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    907.0,
    465.0,
    anchor="nw",
    text="Album",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    904.0,
    525.0,
    anchor="nw",
    text="÷",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    904.0,
    565.0,
    anchor="nw",
    text="1989",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    904.0,
    605.0,
    anchor="nw",
    text="x (Multiply)",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    904.0,
    645.0,
    anchor="nw",
    text="21",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    904.0,
    685.0,
    anchor="nw",
    text="beerbongs & bentleys",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    904.0,
    725.0,
    anchor="nw",
    text="Lemonade",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1238.0,
    465.0,
    anchor="nw",
    text="Duration",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1235.0,
    525.0,
    anchor="nw",
    text="4:23",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1235.0,
    565.0,
    anchor="nw",
    text="3:31",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1235.0,
    605.0,
    anchor="nw",
    text="4:23",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1235.0,
    645.0,
    anchor="nw",
    text="4:50",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1235.0,
    685.0,
    anchor="nw",
    text="3:25",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    1235.0,
    725.0,
    anchor="nw",
    text="3:57",
    fill="#FFFFFF",
    font=("Inter Regular", 14 * -1)
)

canvas.create_text(
    547.0,
    797.0,
    anchor="nw",
    text="Shape of You",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 40 * -1)
)

canvas.create_text(
    896.0,
    813.0,
    anchor="nw",
    text="Ed Sheeran",
    fill="#FFFFFF",
    font=("Inter SemiBold", 24 * -1)
)

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    871.989990234375,
    824.0,
    image=image_image_19
)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(
    78.5,
    93.5,
    image=image_image_20
)

image_image_21 = PhotoImage(
    file=relative_to_assets("image_21.png"))
image_21 = canvas.create_image(
    900.0,
    919.0,
    image=image_image_21
)

image_image_22 = PhotoImage(
    file=relative_to_assets("image_22.png"))
image_22 = canvas.create_image(
    1410.0,
    914.0,
    image=image_image_22
)

image_image_23 = PhotoImage(
    file=relative_to_assets("image_23.png"))
image_23 = canvas.create_image(
    1255.0,
    914.0,
    image=image_image_23
)

image_image_24 = PhotoImage(
    file=relative_to_assets("image_24.png"))
image_24 = canvas.create_image(
    1196.0,
    914.0,
    image=image_image_24
)
window.resizable(False, False)
window.mainloop()
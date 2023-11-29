from tkinter import *
import random
import pandas as pd

BACKGROUND_COLOR = "B1DDC6"
to_learn = {}
current_card = {}
current_direction = "malay_to_english"  # Default direction

# ---------------------- FRONT FLASH CARD FUNCTIONALITY ----------------------- #
# Creating a list of dictionaries from the CSV file using a dataframe

try:
    df = pd.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    df = pd.read_csv("data/en_bm_lesson2_ActionVerbs_v1.csv")
    to_learn = df.to_dict(orient="records")

else:
    to_learn = df.to_dict(orient="records")


def is_known():
    global current_card
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def toggle_direction():
    global current_direction
    if current_direction == "malay_to_english":
        current_direction = "english_to_malay"
        button_direction.config(text="Switch to Malay to English")
    else:
        current_direction = "malay_to_english"
        button_direction.config(text="Switch to English to Malay")


def next_card():
    global current_card, flip_timer
    root.after_cancel(flip_timer)
    current_card = random.choice(to_learn)

    if current_direction == "malay_to_english":
        canvas.itemconfig(card_word, text=current_card["Malay"], fill="black")
        canvas.itemconfig(card_title, text="Malay", fill="black")
    else:
        canvas.itemconfig(card_word, text=current_card["English"], fill="black")
        canvas.itemconfig(card_title, text="English", fill="black")

    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = root.after(3000, func=flip_card)


def flip_card():
    if current_direction == "malay_to_english":
        canvas.itemconfig(card_title, text="English", fill="white")
        canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    else:
        canvas.itemconfig(card_title, text="Malay", fill="white")
        canvas.itemconfig(card_word, text=current_card["Malay"], fill="white")

    canvas.itemconfig(card_background, image=card_back_img)


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Flashcards: Learn Malay")
root.config(pady=20, bg="#B1DDC6", width=900, height=700)

flip_timer = root.after(3000, func=flip_card)

# Card FRONT
canvas = Canvas(width=900, height=600, bg="#B1DDC6")
card_front_img = PhotoImage(file="images/card_front.png", width=800, height=526)
card_back_img = PhotoImage(file="images/card_back.png", width=800, height=526)
card_background = canvas.create_image(450, 280, image=card_front_img)
card_title = canvas.create_text(450, 175, text="Title", font=("Arial", 30, "italic"))
card_word = canvas.create_text(450, 280, text="Word", font=("Arial", 40, "bold"))
canvas.config(bg="#B1DDC6", highlightthickness=0)
canvas.place(x=10, y=20)

# Button wrong
img_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=img_wrong, width=100, height=100, command=next_card)
button_wrong.place(x=300, y=560)

# Button right
img_right = PhotoImage(file="images/right.png")
button_right = Button(image=img_right, width=100, height=100, command=is_known)
button_right.place(x=510, y=560)

next_card()

# Button to toggle direction
button_direction = Button(root, text="Switch to Malay to English", width=25, command=toggle_direction)
button_direction.place(x=350, y=0)

root.mainloop()
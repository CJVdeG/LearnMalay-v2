from tkinter import *
import random
import pandas as pd
import os

BACKGROUND_COLOR = "B1DDC6"
to_learn = {}
current_card = {}
current_direction = "malay_to_english"  # Default direction


# ---------------------- FRONT FLASH CARD FUNCTIONALITY ----------------------- #
# Creating a list of dictionaries from the CSV file using a dataframe


try:
    df = pd.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    df = pd.read_csv("data/1-GettingStarted.csv")
    to_learn = df.to_dict(orient="records")

else:
    to_learn = df.to_dict(orient="records")


# Define a function to initialize the flashcards (used for program restart)
def initialize_flashcards(file_path):
    global to_learn
    try:
        # Check if the file exists and if it is empty
        if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
            # If the file is empty, remove it
            os.remove(file_path)
            raise FileNotFoundError  # Raise FileNotFoundError to load the preconfigured list

        df = pd.read_csv(file_path)
    except FileNotFoundError:
        # If the file doesn't exist or was empty, load the preconfigured list
        df = pd.read_csv("data/1-GettingStarted.csv")

    to_learn = df.to_dict(orient="records")

    if not to_learn:
        # If there are no words to learn, create a new DataFrame from the default file
        df = pd.read_csv("data/1-GettingStarted.csv")
        to_learn = df.to_dict(orient="records")


# Define a function to load the selected file from the dropdown list
def load_selected_file():
    selected_file = selected_file_var.get()
    initialize_flashcards(f"data/{selected_file}")

    # Enable the "Wrong" and "Right" buttons
    button_wrong.config(state=NORMAL)
    button_right.config(state=NORMAL)

    next_card()


# Call this at the beginning of your script to initialize flashcards with a default file
initialize_flashcards("data/1-GettingStarted.csv")


def is_known():
    global current_card
    if current_card in to_learn:
        to_learn.remove(current_card)
        data = pd.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        next_card()
    else:
        # Handle the case when there are no more words to learn
        canvas.itemconfig(card_title, text="Done. Load new file or clear words to learn.")
        canvas.itemconfig(card_word, text="")
        button_right.config(state=DISABLED)  # Disable the "Right" button

        # Optionally, you can also disable the "Wrong" button in this case
        button_wrong.config(state=DISABLED)


def toggle_direction():
    global current_direction
    if current_direction == "malay_to_english":
        current_direction = "english_to_malay"
        button_direction.config(text="Switch to Malay to English")
    else:
        current_direction = "malay_to_english"
        button_direction.config(text="Switch to English to Malay")


def toggle_translation():
    if current_direction == "malay_to_english":
        if canvas.itemcget(card_title, "text") == "Malay":
            canvas.itemconfig(card_title, text="English")
            canvas.itemconfig(card_word, text=current_card["English"])
        else:
            canvas.itemconfig(card_title, text="Malay")
            canvas.itemconfig(card_word, text=current_card["Malay"])
    else:
        if canvas.itemcget(card_title, "text") == "English":
            canvas.itemconfig(card_title, text="Malay")
            canvas.itemconfig(card_word, text=current_card["Malay"])
        else:
            canvas.itemconfig(card_title, text="English")
            canvas.itemconfig(card_word, text=current_card["English"])


def restart_program():
    try:
        os.remove("data/words_to_learn.csv")
    except FileNotFoundError:
        pass
    to_learn.clear()  # Clear the 'to_learn' dictionary
    initialize_flashcards(f"data/{selected_file_var.get()}")  # Load the selected file

    # Enable the "Wrong" and "Right" buttons
    button_wrong.config(state=NORMAL)
    button_right.config(state=NORMAL)

    next_card()  # Load the next card after restarting


def next_card():
    global current_card, flip_timer
    root.after_cancel(flip_timer)

    if to_learn:
        current_card = random.choice(to_learn)
        if current_direction == "malay_to_english":
            canvas.itemconfig(card_word, text=current_card["Malay"], fill="black")
            canvas.itemconfig(card_title, text="Malay", fill="black")
        else:
            canvas.itemconfig(card_word, text=current_card["English"], fill="black")
            canvas.itemconfig(card_title, text="English", fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        flip_timer = root.after(3000, func=flip_card)
    else:
        # Handle the case where there are no more words to learn
        canvas.itemconfig(card_title, text="Done. Load new file or clear words to learn.")
        canvas.itemconfig(card_word, text="")
        button_right.config(state=DISABLED)  # Disable the "Right" button

        # Optionally, you can also disable the "Wrong" button in this case
        button_wrong.config(state=DISABLED)

        # Load the selected file from the dropdown list
        initialize_flashcards(f"data/{selected_file_var.get()}")


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
root.config(pady=20, bg="#B1DDC6", width=1300, height=600)

flip_timer = root.after(3000, func=flip_card)

# Card FRONT
canvas = Canvas(width=900, height=600, bg="#B1DDC6")
card_front_img = PhotoImage(file="images/card_front.png", width=800, height=526)
card_back_img = PhotoImage(file="images/card_back.png", width=800, height=526)
card_background = canvas.create_image(450, 280, image=card_front_img)
card_title = canvas.create_text(450, 100, text="Title", font=("Arial", 25, "italic"))
card_word = canvas.create_text(450, 200, text="Word", font=("Arial", 30, "bold"), width=700)
canvas.config(bg="#B1DDC6", highlightthickness=0)
canvas.place(x=10, y=20)


# ---------------------------- BUTTONS FOR RIGHT AND WRONG ------------------------------- #
# Button wrong
img_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=img_wrong, width=100, height=100, command=next_card)
button_wrong.place(x=320, y=360)

# Button right
img_right = PhotoImage(file="images/right.png")
button_right = Button(image=img_right, width=100, height=100, command=is_known)
button_right.place(x=470, y=360)

# ---------------------------- BUTTONS FOR FUNCTIONS ------------------------------- #

# Button to toggle direction
button_direction = Button(root, text="Switch to Malay to English", font=("Arial", 15, "bold"), width=25, command=toggle_direction)
button_direction.place(x=900, y=50)

# Button to toggle translation
button_toggle = Button(root, text="Toggle Translation", font=("Arial", 15, "bold"), width=25, command=toggle_translation)
button_toggle.place(x=900, y=100)

# Button to restart the program
button_restart = Button(root, text="Clear words to learn", font=("Arial", 15, "bold"), width=25, command=restart_program)
button_restart.place(x=900, y=150)

# Add a dropdown list to select the file
available_files = os.listdir("data")
available_files.sort()  # Sort the list alphabetically
selected_file_var = StringVar(root)
selected_file_var.set("1-GettingStarted.csv")  # Default selection
file_dropdown = OptionMenu(root, selected_file_var, *available_files)
file_dropdown.configure(font=("Arial", 14, "normal"), width=25)  # Apply font and width styling
file_dropdown.place(x=900, y=250)

# Button to load the selected file
load_file_button = Button(root, text="Load selected File", font=("Arial", 14, "normal"), width=25, command=load_selected_file)
load_file_button.place(x=900, y=300)

# ---------------------------- LOAD THE PROGRAM ------------------------------- #

next_card()

root.mainloop()
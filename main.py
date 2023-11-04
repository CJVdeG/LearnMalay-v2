# Google text to voice libraries
from gtts import gTTS
from playsound import playsound
import tempfile

from tkinter import ttk
from tkinter import *
import random
import pandas as pd
import os


BACKGROUND_COLOR = "B1DDC6"
to_learn = {}
current_card = {}
current_direction = "malay_to_english"  # Default direction

# Create a variable to track the "Auto-pronounce" feature state
auto_pronounce = False

# ---------------------- FRONT FLASH CARD FUNCTIONALITY ----------------------- #
# Creating a list of dictionaries from the CSV file using a dataframe


try:
    dataframe = pd.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    dataframe = pd.read_csv("data/1-GettingStarted.csv")
    to_learn = dataframe.to_dict(orient="records")

else:
    to_learn = dataframe.to_dict(orient="records")


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


# Call this at the beginning of the script to initialize flashcards with a default file
initialize_flashcards("data/words_to_learn.csv")


# Google Text to Speech
# Updated text_to_speech function to consider the "Auto-pronounce" and manual pronunciation
def text_to_speech(text, manual=False):
    if (not hasattr(text_to_speech, "pronounced") or not text_to_speech.pronounced) or manual:
        tts = gTTS(text, lang='ms')  # Pronounce Malay words
        temp_file = tempfile.NamedTemporaryFile(delete=True)
        tts.save(temp_file.name + ".mp3")
        playsound(temp_file.name + ".mp3")
        if not manual:
            text_to_speech.pronounced = True


# Function to show the number of remaining words
def get_remaining_words_count():
    try:
        df = pd.read_csv("data/words_to_learn.csv")
        return len(df)
    except FileNotFoundError:
        return 0


# Function to toggle the "Auto-pronounce" feature
def toggle_auto_pronounce():
    global auto_pronounce
    auto_pronounce = auto_pronounce_var.get()


def is_known():
    global current_card
    if current_card in to_learn:
        to_learn.remove(current_card)
        data = pd.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        next_card()
        word_count_label.config(text=f"Words to Learn: {get_remaining_words_count()}")
    else:
        # Handle the case when there are no more words to learn
        canvas.itemconfig(card_title, text="Done. Load new file or clear words to learn.")
        canvas.itemconfig(card_word, text="")
        button_right.config(state=DISABLED)  # Disable the "Right" button

        # Optionally, you can also disable the "Wrong" button in this case
        button_wrong.config(state=DISABLED)


# In the "toggle_direction" function, update the "Auto-pronounce" state
def toggle_direction():
    global current_direction
    global auto_pronounce
    if current_direction == "malay_to_english":
        current_direction = "english_to_malay"
        button_direction.config(text="Switch to English to Malay")
        # Disable "Auto-pronounce" when the direction changes
        auto_pronounce = False
    else:
        current_direction = "malay_to_english"
        button_direction.config(text="Switch to Malay to English")


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

    # Update the word count label
    word_count_label.config(text=f"Words to Learn: {get_remaining_words_count()}")


# In the "next_card" function, call the text_to_speech function for the first card
def next_card():
    global current_card, flip_timer
    root.after_cancel(flip_timer)

    # Reset the 'pronounced' attribute each time a new card is displayed
    text_to_speech.pronounced = False

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

        # Check if "Auto-pronounce" is enabled and the direction is "malay_to_english"
        if auto_pronounce and current_direction == "malay_to_english":
            # Delay the pronunciation by 1000 milliseconds (1 second)
            root.after(1000, lambda: text_to_speech(current_card["Malay"]))
    else:
        canvas.itemconfig(card_title, text="Done. Load new file or clear words to learn")
        canvas.itemconfig(card_word, text="")
        button_right.config(state=DISABLED)
        button_wrong.config(state=DISABLED)
        initialize_flashcards(f"data/{selected_file_var.get()}")


# In the "flip_card" function, call the text_to_speech function
def flip_card():
    if current_direction == "malay_to_english":
        canvas.itemconfig(card_title, text="English", fill="white")
        canvas.itemconfig(card_word, text=current_card["English"], fill="white")

        # Pronounce the Malay word if "Auto-pronounce" is enabled
        text_to_speech(current_card["Malay"])

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
button_direction = Button(root, text="Switch to English to Malay", font=("Arial", 15, "bold"), width=25, command=toggle_direction)
button_direction.place(x=900, y=50)

# Button to toggle translation
button_toggle = Button(root, text="Toggle Translation", font=("Arial", 15, "bold"), width=25, command=toggle_translation)
button_toggle.place(x=900, y=100)

# Button to restart the program
button_restart = Button(root, text="Clear words to learn", font=("Arial", 15, "normal"), width=25, command=restart_program)
button_restart.place(x=900, y=450)

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

# Button for Google text to speech
pronounce_button = Button(root, text="Pronounce", font=("Arial", 14, "bold"), width=25, command=lambda: text_to_speech(current_card["Malay"], manual=True))
pronounce_button.place(x=900, y=150)

# Show how many words remain in words to learn list
word_count_label = Label(root, text=f"Words to Learn: {get_remaining_words_count()}", font=("Arial", 14))
word_count_label.place(x=900, y=420)

# NEW on/off switch Toggle button for "Auto-pronounce"
# -------- Auto Pronounce Check Button --------#

# Create a BooleanVar to track the state of Auto Pronounce
auto_pronounce_var = BooleanVar()
auto_pronounce_var.set(auto_pronounce)  # Initialize the state

# Create a style for the Auto pronounce checkbox button
style = ttk.Style()
style.configure("TCheckbutton", font=("Arial", 15))
# Replace the "Toggle button for Auto-pronounce" section
auto_pronounce_switch = ttk.Checkbutton(root, text="Auto Pronounce?", variable=auto_pronounce_var, command=toggle_auto_pronounce)
auto_pronounce_switch.place(x=900, y=500)

# ---------------------------- LOAD THE PROGRAM ------------------------------- #

next_card()

root.mainloop()

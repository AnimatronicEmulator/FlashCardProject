import pandas
from tkinter import *
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


# ---------------------------- LOAD FLASH CARDS ------------------------------- #
try:
    new_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/dutch_words.csv")
    flash_cards = original_data.to_dict(orient="records")
else:
    flash_cards = new_data.to_dict(orient="records")


# ---------------------------- PROBLEM WORDS ------------------------------- #
def future_study_deck():
    flash_cards.remove(current_card)
    words_to_learn = pandas.DataFrame(flash_cards)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    new_card()


# ---------------------------- RANDOM WORD PICKER ------------------------------- #
def new_card():
    global flip_timer, current_card
    window.after_cancel(flip_timer)
    current_card = random.choice(flash_cards)
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(title_text, text="Dutch", fill="black")
    canvas.itemconfig(word_text, text=current_card["dutch"], fill="black")
    flip_timer = window.after(3000, card_flip)


# ---------------------------- CARD FLIP ------------------------------- #
def card_flip():
    english_word = flash_cards[current_card]["english"]
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=english_word, fill="white")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, card_flip)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, command=new_card, bg=BACKGROUND_COLOR, borderwidth=0)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, command=future_study_deck, bg=BACKGROUND_COLOR, borderwidth=0)
right_button.grid(row=1, column=1)

new_card()

window.mainloop()

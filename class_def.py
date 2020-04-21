import os
import random
from time import sleep
from tkinter import *

from PIL import Image, ImageTk

directory = './card_images/single_card'

class Deck():
    def __init__(self):
        self.deck = {}
        for file in os.listdir(directory):
            file_name = "card_images/single_card/"+file  
            image = ImageTk.PhotoImage((Image.open(file_name)).resize((100, 150), Image.ANTIALIAS))
            self.deck[image] = file.strip(".jpg")

    def shuffle(self):
        return random.sample(list(self.deck.keys()), len(list(self.deck.keys())))

    def create_dummy_set(self):
        dummy_deck = []
        for i in range(54):
            image = ImageTk.PhotoImage((Image.open("card_images/group_cards/red_back.jpg")).resize((100, 150), Image.ANTIALIAS))
            dummy_deck.append(image)
        return dummy_deck

class Person():
    def __init__(self):
        self.deck_ref = {}
        self.deck = []
        self.life = 40
    
    def draw(self, root, canvas, deck_position, full_deck, deck, num_cards, start, space, bottom):
        text_id = canvas.create_text(100,200, fill="black", font="Times 20 bold", text="Dealing 7 Cards...")
        root.after(1000, lambda: canvas.delete(text_id))
        root.update()
        for i, position in reversed(list(enumerate(deck_position[(len(deck_position)-num_cards):]))):
            self.move_card(canvas, position, (start + ((num_cards-1)-i)*space), bottom)
            sleep(0.5)
            # print(full_deck[deck[len(deck) - ((num_cards-1)-i) - 1]])
            self.deck_ref[deck[-1]] = full_deck[deck[-1]]
            self.deck.append(deck[-1])
            canvas.itemconfig(position, image = self.deck[-1])
            canvas.lift(position)
            canvas.tag_bind(position, '<B1-Motion>', lambda event, arg=canvas: self.onObjectMove(event, arg))
            canvas.tag_bind(position, '<ButtonRelease-1>', lambda event, arg=canvas, arg1=position: self.onObjectRelease(event, arg, arg1))
            deck.pop(-1)
            root.update()

            

    def move_card(self, canvas, position, x, y):
        canvas.move(position, x, y)

    def onObjectMove(self, event, canvas):                  
        current = event.widget.find_withtag('current')[0]
        self.move_card(canvas, current, event.x-((canvas.coords(current))[0]), event.y-((canvas.coords(current))[1]))

    def onObjectRelease(self, event, canvas, position): 
        # canvas.tag_unbind(position, '<B1-Motion>')
        pass

from tkinter import *
from PIL import ImageTk, Image
from class_def import *
from time import sleep

class MyCardGame:
    def __init__(self):
        self.canvas = Canvas(root, width = 1800, height = 1800)      
        self.canvas.pack() 
        self.deck_object = Deck() 
        self.deck = self.deck_object.shuffle()
        self.dummy_deck = self.deck_object.create_dummy_set()
        self.deck_position = []
        self.people = []

        for i, image in enumerate(self.dummy_deck):
            self.deck_position.append(self.canvas.create_image(i*25, 0, image=image, anchor=NW))
            
        root.update()
        sleep(1)
        self.people.append(Person(self.canvas))
        self.people[-1].draw(root, self.canvas, self.deck_position, self.deck_object.deck, self.deck, 7, 0, 25, 700)
            

root = Tk()
my_gui = MyCardGame()
root.mainloop()
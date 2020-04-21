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

        # for i, image in enumerate(self.deck):
        #     self.deck_position.append(self.canvas.create_image(i*25, 0, image=image, anchor=NW))
        for i, image in enumerate(self.dummy_deck):
            self.deck_position.append(self.canvas.create_image(i*25, 0, image=image, anchor=NW))
        # text_id = self.canvas.create_text(100,300,fill="darkblue",font="Times 20 italic bold",
        #                 text="Dealing 7 Cards...")
        # sleep(2)
        # self.canvas.delete(text_id)
        root.update()
        sleep(1)
        person1 = Person()
        person1.draw(root, self.canvas, self.deck_position, self.deck_object.deck, self.deck, 7, -1320, 60, 700)
        # text_id = self.canvas.create_text(100,200, fill="black", font="Times 20 bold", text="Dealing 7 Cards...")
        # root.after(1000, lambda: self.canvas.delete(text_id))
        # root.update()
        
        # for i, position in reversed(list(enumerate(self.deck_position[(len(self.deck_position)-7):]))):
        #     self.move_card(position, (-1320 - (i-6)*45), 700)
        #     sleep(0.5)
            

root = Tk()
my_gui = MyCardGame()
root.mainloop()
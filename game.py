from tkinter import *
from PIL import ImageTk, Image
from class_def import *
from time import sleep

class MyCardGame:
    def __init__(self):
        self.canvas = Canvas(root, width = 1800, height = 1300)      
        self.canvas.pack(pady=0) 
        self.deck_object = Deck() 
        self.deck = self.deck_object.shuffle()
        self.dummy_deck = self.deck_object.create_dummy_set()
        self.deck_position = []
        self.people = []

        for i, image in enumerate(self.dummy_deck):
            self.deck_position.append(self.canvas.create_image(i*5 , 418, image=image, anchor=CENTER))
            
        root.update()
        sleep(1)
        self.people.append(Human(self.canvas, [500, 590, 465, 610], [500, 590, 655, 800]))
        self.people.append(AI(self.canvas, [500, 590, 225, 370], [500, 590, 35, 180]))
        root.update()
        self.intial_draw()
    
    def intial_draw(self):
        for i in range(0, 7*len(self.people), len(self.people)):
            self.people[0].draw(root, self.canvas, self.deck_position, self.deck_object.deck, self.deck, i, int(i/len(self.people)), 45, 25, 770)
            self.people[1].draw(root, self.canvas, self.deck_position, self.deck_object.deck, self.deck, i+1, int(i/len(self.people)), 45, 25, 70)
        self.people[0].turn(self.canvas, root)
        #self.people[0].unbind_events_single(self.canvas, self.deck_position)
        #self.people[0].attack(self.canvas, root)

root = Tk()
my_gui = MyCardGame()
root.mainloop()
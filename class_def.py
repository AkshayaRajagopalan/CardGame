import os
import random
from time import sleep
from tkinter import *
import math

from PIL import Image, ImageTk

directory = './card_images/single_card'

class Deck():
    def __init__(self):
        self.deck = {}
        for file in os.listdir(directory):
            file_name = "card_images/single_card/"+file  
            image = ImageTk.PhotoImage((Image.open(file_name)).resize((80, 130), Image.ANTIALIAS))
            self.deck[image] = file[:-4]

    def shuffle(self, deck = []):
        if(len(deck) != 0):
            return random.sample(list(deck.keys()), len(list(deck.keys())))
        else:
            return random.sample(list(self.deck.keys()), len(list(self.deck.keys())))

    def create_dummy_set(self):
        dummy_deck = []
        for i in range(54):
            image = ImageTk.PhotoImage((Image.open("card_images/group_cards/red_back.jpg")).resize((80, 130), Image.ANTIALIAS))
            dummy_deck.append(image)
        return dummy_deck

class Person():
    def __init__(self, canvas, monster_coords, trap_coords):
        self.deck_ref = {}
        self.deck = []
        self.life = 40
        self.MonsterSlots = []
        self.TrapSlots = []
        for i in range(3):
            self.MonsterSlots.append(MonsterSlot(canvas, monster_coords[0]+i*200, monster_coords[1]+i*200, monster_coords[2], monster_coords[3]))
            self.TrapSlots.append(TrapSlot(canvas, trap_coords[0]+i*200, trap_coords[1]+i*200, trap_coords[2], trap_coords[3]))

    
    def draw(self, root, canvas, deck_position, full_deck, deck, card_number, num_cards, start, space, bottom):
        text_id = canvas.create_text(100,200, fill="black", font="Times 20 bold", text="Dealing 7 Cards...")
        root.after(1000, lambda: canvas.delete(text_id))
        root.update()
        self.move_card(canvas, deck_position[53 - card_number], (start + (card_number*space)/2), bottom)
        sleep(0.5)

        self.deck_ref[deck[53 - card_number]] = full_deck[deck[53 - card_number]]
        self.deck.append(deck[53 - card_number])
        canvas.itemconfig(deck_position[53 - card_number], image = self.deck[num_cards])
        canvas.lift(deck_position[53 - card_number])
        self.bind_events(canvas, deck_position[53 - card_number], deck_position, full_deck)

        root.update()

    def bind_events(self, canvas, position, deck_position, full_deck):
        canvas.tag_bind(position, '<B1-Motion>', lambda event, arg=canvas: self.onObjectMove(event, arg))
        canvas.tag_bind(position, '<ButtonRelease-1>', lambda event, arg=canvas, arg1=[canvas.coords(i) for i in deck_position], arg2=full_deck: self.onObjectRelease(event, arg, arg1, arg2))      

    def unbind_events_single(self, canvas, position):
        canvas.tag_unbind(position, '<B1-Motion>')
        canvas.tag_unbind(position, '<ButtonRelease-1>')
    
    def move_card(self, canvas, position, x, y, x_offset = 0, y_offset = 0):
        canvas.coords(position, x + x_offset, y + y_offset)

    def onObjectMove(self, event, canvas):                  
        current = event.widget.find_withtag('current')[0]
        for monster, trap in zip(self.MonsterSlots, self.TrapSlots):
           if monster.check_eligibility(list(self.deck_ref.values())[math.floor((54 - int(current))/2)]):
               canvas.itemconfig(monster.slot, fill='#00cc29', outline="#00cc29")
           if trap.check_eligibility(list(self.deck_ref.values())[math.floor((54 - int(current))/2)]):
               canvas.itemconfig(trap.slot, fill='#00cc29', outline="#00cc29")
        self.move_card(canvas, current, event.x, event.y)



    def onObjectRelease(self, event, canvas, deck_prev_position, full_deck): 
        current = event.widget.find_withtag('current')[0]
        overlap_monster = [i.check_slot_criterion(canvas, event.x, event.y, list(self.deck_ref.values())[math.floor((54 - int(current))/2)], current) for i in self.MonsterSlots]
        overlap_trap = [i.check_slot_criterion(canvas, event.x, event.y, list(self.deck_ref.values())[math.floor((54 - int(current))/2)], current) for i in self.TrapSlots]
        if True in overlap_monster:
            coordinates_monster = canvas.coords((self.MonsterSlots[overlap_monster.index(True)]).slot)
            if ((self.MonsterSlots[overlap_monster.index(True)]).fused):
                self.move_card(canvas, current, (coordinates_monster[0] + coordinates_monster[2])/2.0 , (coordinates_monster[1] + coordinates_monster[3])/2.0, (len((self.MonsterSlots[overlap_monster.index(True)]).cards) - 1)*15)
                canvas.lift(current)
            else:
                self.move_card(canvas, current, (coordinates_monster[0] + coordinates_monster[2])/2.0 , (coordinates_monster[1] + coordinates_monster[3])/2.0)

            deck_prev_position[int(current) - 1] = canvas.coords(current)
            self.unbind_events_single(canvas, current)
        
        elif True in overlap_trap:
            coordinates_trap = canvas.coords((self.TrapSlots[overlap_trap.index(True)]).slot)
            self.move_card(canvas, current, (coordinates_trap[0] + coordinates_trap[2])/2.0 , (coordinates_trap[1] + coordinates_trap[3])/2.0)
            deck_prev_position[int(current) - 1] = canvas.coords(current)
            self.unbind_events_single(canvas, current)

        else:
            self.move_card(canvas, current, deck_prev_position[int(current) - 1][0], deck_prev_position[int(current) - 1][1])
        
        for monster, trap in zip(self.MonsterSlots, self.TrapSlots):
            canvas.itemconfig(monster.slot, fill="#b8a800", outline="#b8a800")
            canvas.itemconfig(trap.slot, fill="black", outline="black")

class MonsterSlot():
    def __init__(self, canvas, x1, x2, y1, y2):
        self.slot = canvas.create_rectangle(x1, y1, x2, y2, fill="#b8a800", outline="#b8a800")
        self.value = 0
        self.occupied = False
        self.cards = []
        self.card_positions = {}
        self.fused = False


    def check_slot_criterion(self, canvas, x, y, card, id):
        if self.check_eligibility(card) and self.check_slot(canvas, x, y):
            self.cards.append(card)
            self.fused = self.occupied
            self.card_positions[card] = id
            self.occupied = True
            self.value += int(card[:-1])
            return True
        return False

    def check_eligibility(self, card):
        if (any(substring in card for substring in ["2", "3", "4", "5", "6", "7", "8", "9", "10"])) and ("joker" not in card) :
            contains = [True for i in self.cards if card[:-1] in i] 
            if self.occupied == False or (self.occupied == True and (len(contains) == len(self.card_positions))):
                return True
        return False

    def check_slot(self, canvas, x, y):
        if canvas.coords(self.slot)[0] <= x and canvas.coords(self.slot)[1] <= y and canvas.coords(self.slot)[2] >= x and canvas.coords(self.slot)[3] >= y:
            return True
        return False
    
class TrapSlot():
    def __init__(self, canvas, x1, x2, y1, y2):
        self.slot = canvas.create_rectangle(x1, y1, x2, y2, fill="black")
        self.occupied = False
        self.card = ""
        self.card_position = 0


    def check_slot_criterion(self, canvas, x, y, card, id):
        if canvas.coords(self.slot)[0] <= x and canvas.coords(self.slot)[1] <= y and canvas.coords(self.slot)[2] >= x and canvas.coords(self.slot)[3] >= y:
            if self.check_eligibility(card):
                    self.card = card[:-1]
                    self.card_position= id
                    self.occupied = True
                    return True
        return False

    def check_eligibility(self, card):
        if (any(substring in card for substring in ["K", "Q", "J", "joker", "A"])) :
            if self.occupied == False:
                return True
        return False

class Human(Person):
    def __init__(self, canvas, monster_coords, trap_coords):
        super(Human, self).__init__(canvas, monster_coords, trap_coords)


class AI(Person):
    def __init__(self, canvas, monster_coords, trap_coords):
        super(AI, self).__init__(canvas, monster_coords, trap_coords)

    def bind_events(self, canvas, position, deck_position, full_deck):
        pass

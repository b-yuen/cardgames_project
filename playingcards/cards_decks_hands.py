#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 17:14:11 2022

@author: benjaminyuen
"""

import numpy as np

class card:
    
    ranks = {0:2,1:3,2:4,3:5,4:6,5:7,6:8,7:9,8:10,9:'Jack',10:'Queen',11:'King',12:'Ace'}
    suits = {0:'Spades', 1:'Clubs', 2:'Diamonds', 3:'Hearts'}
    
    def __init__(self, card_id):
        self.check_id(card_id)
        self.id = card_id
        self.rank_id = int(self.id / 4)
        self.suit_id = self.id % 4
#        self.value = self.calc_value()
        self.value = self.id
        
    def check_id(self, card_id):
        if not 0 <= card_id <= 51:
            raise Exception('Invalid card id. Must be in range [0,51]')
            
#    def calc_value(self):
##        rank_id = self.id % 13
#        rank_id = int(self.id / 4)
##        suit_id = int(self.id / 13)
#        suit_id = self.id % 4
#        val = 4 * rank_id + suit_id
#        return val
    
    def rank(self):
#        rank_id = self.id % 13
#        rank_id = int(self.id / 4)
#        return card.ranks[rank_id]
        return card.ranks[self.rank_id]
        
    def suit(self):
##        suit_id = int(self.id / 13)
#        suit_id = self.id % 4
#        return card.suits[suit_id]
        return card.suits[self.suit_id]
    
    def is_face(self):
        return type(self.rank()) == str
    
    def __str__(self):
        return str(self.rank()) + ' of ' + self.suit()
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value
    
class deck:
    def __init__(self):
        self.make_deck()
        
    def make_deck(self):
        self.cards = np.array([card(i) for i in range (52)])
            
    def deal(self, n):
        # deals n cards from deck, returning the card ids
        if n > len(self.cards):
            raise Exception('Too few cards ramining in deck')
        self.justdealt = np.random.choice(self.cards, size = n, replace = False)
        self.removecards(self.justdealt)
        return self.justdealt
        
    def removecards(self, cardstoremove):
        newdeck = np.array([], dtype = object)
        for el in self.cards:
            if el not in cardstoremove: # check in by value no by object id due to __eq__ method in card
                newdeck = np.append(newdeck, el)
        self.cards = newdeck
        
class hand:
    def __init__(self, obj_array):
        # obj_array should be a numpy 1D array of card objects
        self.cards = obj_array
        
    def findpairs(self):
        self.pairs = []
        has_pairs = False
        for i in range(len(self.cards)):
            card_i = self.cards[i]
            for j in range(i+1, len(self.cards)):
                card_j = self.cards[j]
                if card_i.rank() == card_j.rank():
                    pair = [[card_i, card_j]]
                    self.pairs = self.pairs + pair
                    has_pairs = True
        self.pairs = np.array(self.pairs)
        return has_pairs
    
    def pair_value(self, pair):
        (c1, c2) = pair
        return max(c1.value, c2.value)
        
        
class two_card_hand(hand):
    def __init__(self, obj_array):
        super().__init__(obj_array)
        if len(obj_array) != 2:
            raise Exception("input array must contain exactly two cards")
        self.value = self.calc_value()
        
    def calc_value(self):
        if self.findpairs():
            value = 51 + self.pair_value(self.pairs[0])
        else:
            value = max(self.cards[0].value, self.cards[1].value)
        return value
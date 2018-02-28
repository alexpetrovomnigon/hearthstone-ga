from hearthstone.deckstrings import parse_deckstring
from hearth.card.cards import Cards
from hearth.hand.hand import Hand

import random

class Deck:
    _cards = []
    _hero = None
    _type = None
    _fitness = None
    def __init__(self, deckstring = ""):
        self._cards = []
        if deckstring:
            cards = parse_deckstring(deckstring)

            self._hero = Cards().getById(cards[1][0])
            self._type = cards[2]
            for card in cards[0]:
                self._cards.append(Cards().getById(card[0]))
                if(card[1] == 2):
                    self._cards.append(Cards().getById(card[0]))

    def addCard(self, card):
        self._cards.append(card)

    def getSize(self):
        return len(self._cards)

    def getStrength(self):
        strength = 0
        for card in self._cards:
            strength += card.getStrength(self)
        return strength

    def getTotalManaCost(self):
        cost = 0
        for card in self._cards:
            cost += card.cost
        return cost

    def getFitness(self):
        if self._fitness == None:
            cost = self.getTotalManaCost()
            strength = self.getStrength()
            self._fitness = 55 * strength / cost
        return self._fitness

    def hasCards(self):
        return len(self._cards)

    def drawCard(self):
        if len(self._cards):
            card = random.choice(self._cards)
            if(card in self._cards):
                self._cards.remove(card)
            print(card.name, " drawn")
            return card
        return None

    def drawCardOfType(self):
        return None
    def drawCardOfRace(self):
        return None
    def drawCardOfMechanic(self):
        return None

    def averageMinionHealth(self):
        sum = 0
        count = 0
        for card in self._cards:
            if card.type == "MINION":
                sum += card.health
                count += 1
        if count:
            return sum/count
        else:
            return 0

    def averageMinionLifespan(self):
        health = self.averageMinionHealth()
        if health < 3:
            return 1
        return health / 2

    def numberOfXCostCard(self, x):
        number = 0
        for card in self._cards:
            if card.cost == x:
                number += 1
        return number

    def numberOfCardsOfRace(self, race):
        number = 0
        for card in self._cards:
            if card.race == race:
                number += 1
        return number

    def numberOfCardsOfType(self, type):
        number = 0
        for card in self._cards:
            if card.type == type:
                number += 1
        return number

    def numberOfCardsOfMechanic(self, mechanic):
        number = 0
        for card in self._cards:
            if mechanic in card.mechanics:
                number += 1
        return number

    def numberofCardsWithDescriptionContainingText(self, text):
        numberMatching = 0
        for card in self._cards:
            if text in card.text:
                numberMatching += 1
        return numberMatching

    def numberOfSpellsDealingDamage(self):
        number = 0
        for card in self._cards:
            if card.type == "SPELL" and "Deal" in card.text:
                number += 1
        return number

    def hasCardWithName(self, name):
        for card in self._cards:
            if card.name == name:
                return True
        return False

    def isValid(self):
        for cardOne in self._cards:
            encounters = 0
            for cardTwo in self._cards:
                if cardOne.name == cardTwo.name:
                    encounters += 1
            if cardOne.rarity == "LEGENDARY":
                if encounters > 1:
                    return False
            else:
                if encounters > 2:
                    return False
        return True

    def printDeck(self):
        print("!-------------------------------!")
        for card in self._cards:
            print(card.name)
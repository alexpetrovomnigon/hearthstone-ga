from hearthstone.deckstrings import parse_deckstring

from hearth.card.cards import Cards
import random

#hero powers

#priest Lesser heal 479
#warrior Armor Up! 725
#mage fireblast 807
#paladin reinforce 472
#druid shapeshift 1123
#shaman Totemic Call 687
#rogue Dagger Mastery 730
#warlock Life Tap 300
#hunter Steady Shot 229

class Hand:
    _deck = None
    _hand = []
    _board = []
    _hero = None
    _heroPower = None
    _speed = 1
    _boardValue = 0
    _damageDealt = 0
    _mana = 0
    _remainingMana = 0
    _health = 30
    def __init__(self, deck):
        self._deck = deck
        self._hero = deck._hero

    def emulateTurn(self):
        print("Starting turn")
        #increase mana
        if self._mana < 10:
            self._mana += 1

        #restore mana
        self._remainingMana = self._mana
        print("Mana ", self._mana)
        #draw a card
        for i in range(0, self._speed):
            card = self._deck.drawCard()
            if len(self._hand) < 10:
                self._hand.append(card)

        # while there is still mana
        # select a card and play it
        # triggering battlecry is handled within Card class
        cardToPlay = self.getRandomCardToPlay()
        while cardToPlay:
            cardToPlay.play(self)
            cardToPlay = self.getRandomCardToPlay()

            #emulate opponents turn - dealing damage equals to 1.5 opponents mana
            #triggering deathrattle is handled in card
            self.emulateDamage()

        return 0

    def emulateGame(self):
        print("Starting game")
        self._deck.drawCard()
        self._deck.drawCard()
        self._deck.drawCard()
        while self._deck.hasCards() and self._health > 0 and self._mana < 10:
            self.emulateTurn()

    def getRandomCardToPlay(self):
        availableCards = []
        for card in self._hand:
            if len(self._board) == 7 and card.type == "MINION":
                continue
            if card.cost < self._remainingMana:
                availableCards.append(card)
        if len(availableCards):
            card = random.choice(availableCards)
            if(card in self._hand):
                self._hand.remove(card)
            print(card.name, " selected to be played")
            return card
        return None

    def emulateDamage(self):
        damageAbsorbed = 0
        damageLeft = round(self._mana * 1.5);
        while damageLeft > 0:
            if len(self._board):
                target = random.choice(self._board)
                if(target.health >= damageLeft):
                    target.takeDamage(damageLeft, hand)
                    damageAbsorbed += damageLeft
                    damageLeft = 0
                else:
                    target.takeDamage(target.health, hand)
                    damageAbsorbed += target.health
                    damageLeft -= target.health
            else:
                self.takeDamage(damageLeft)
                damageAbsorbed += damageLeft
                damageLeft = 0

    def takeDamage(self, damage):
        return 0;
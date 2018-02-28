from hearthstone.enums import GameTag, CardClass, CardSet, Rarity, ZodiacYear
import hearth.strategies.strategies
import types
import hearth.strategies.strategies as strategies

class Card:
    artist = ''
    cardClass = ''
    collectible = False
    cost = 0
    dbfId = 0
    flavor = ''
    id = ''
    name = ''
    playRequirements = []
    playerClass = ''
    rarity = ''
    set = ''
    text = ''
    type = ''
    mechanics = []
    attack = 0
    health = 0
    referencedTags = []
    race = ''
    elite = False
    targetingArrowText = ''
    durability = 0
    overload = 0
    spellDamage = 0
    howToEarn = ''
    howToEarnGolden = ''
    hideStats = False
    entourage = []
    collectionText = ''
    classes = []
    multiClassGroup = ''
    faction = ''
    armor = 0

    damaged = False
    lifesteal = False

    _strengthStrategyName = None
    _battlecryStrategyName = None
    _deathrattleStrategyName = None
    _playStrategyName = None

    def __init__(self, card_data):
        try:
            keys = list(card_data.keys())
            for key in keys[:]:
                if key == "collectible" or key == "":
                    setattr(self, key, True)
                else:
                    setattr(self, key, card_data[key])

            self._strengthStrategyName = self._getStrategyName() + "Strength"
            self._battlecryStrategyName = self._getStrategyName() + "Battlecry"
            self._deathrattleStrategyName = self._getStrategyName() + "Deathrattle"
            self._playStrategyName = self._getStrategyName() + "Play"
        except KeyError:
            print("KeyError")
        return None

    def _getStrategyName(self):
        name = self.name
        name = name.replace(" ", "")
        name = name.replace("-", "")
        name = name.replace("'", "")
        name = name.replace(",", "")
        name = name.replace(":", "")
        name = name.replace(".", "")
        name = name.replace("!", "")
        name = name.replace("?", "")
        return name

    def getDefaultStrength(self, deck):
        strength = 0
        if "DISCOVER" in self.referencedTags:
            strength += 3
        if "ADAPT" in self.referencedTags:
            strength += 5
        if "SPELLPOWER" in self.referencedTags:
            strength += deck.numberOfSpellsDealingDamage()
        if "TAUNT" in self.mechanics:
            strength += 1
        if "DIVINE_SHIELD" in self.mechanics:
            strength += self.attack + 1
        if "WINDFURY" in self.mechanics:
            strength += self.attack * 2
        if "STEALTH" in self.mechanics:
            strength += self.attack
        if "LIFESTEAL" in self.mechanics:
            strength += self.attack
        if "CHARGE" in self.referencedTags:
            strength += self.attack
        if "CANT_BE_TARGETED_BY_SPELLS" in self.mechanics:
            strength += 1
        if "CANT_BE_TARGETED_BY_HERO_POWERS" in self.mechanics:
            strength += 1
        if "POISONOUS" in self.mechanics:
            strength += 5
        if "COMBO" in self.mechanics:
            strength += 5
        if "ADAPT" in self.mechanics:
            strength += 5

        if(self.type == "MINION"):
            strength += self.health + self.attack
            return strength
        else:
            return strength

    def getStrengthByDescription(self, deck):
        strength = 0
        for card in deck._cards:
            #race
            races = ["Dragon", "Murloc", "Pirate", "Totem", "Beast", "Demon", "Mech", "Elemental"]
            for race in races:
                if race in self.text:
                    strength += deck.numberOfCardsOfRace(race.upper())
            if "Whenever you play a card, give" in self.text:
                strength += 5
            #mechanics
            if "<b>Battlecry</b> minions" in self.text:
                strength += deck.numberOfCardsOfMechanic("BATTLECRY")
            if "<b>Deathrattle</b> minions" in self.text:
                strength += deck.numberOfCardsOfMechanic("DEATHRATTLE")
            if "<b>Taunt</b> minions" in self.text:
                strength += deck.numberOfCardsOfMechanic("TAUNT")
            if "<b>Charge</b> minions" in self.text:
                strength += deck.numberOfCardsOfMechanic("CHARGE")
            #type
            if "your weapon" in self.text:
                strength += deck.numberOfCardsOfType("WEAPON")
            if "spell" in self.text:
                strength += deck.numberOfCardsOfType("SPELL")
            if "your minion" in self.text:
                strength += deck.numberOfCardsOfType("MINION")
        return strength

    def getStrength(self, deck):
        strength = self.getDefaultStrength(deck)
        strength += self.getStrengthByDescription(deck)
        method_to_call = getattr(strategies, self._strengthStrategyName)
        strength += method_to_call(self, deck)
        return strength

    def takeDamage(self, amount, hand):
        print(self.name, " takes ", amount, " of damage")
        if self.type == "MINION":
            self._health -= amount
            if self._health <= 0:
                self.die(hand)

    def play(self, hand):
        print("Played: ", self.name)
        self._battlecryStrategyName(self, hand)
        hand._board.append(self)

    def die(self, hand):
        print("Died: ", self.name)
        self._deathrattleStrategyName(self, hand)
        hand._board.remove(self)

    def __str__(self):
        return self.name + "\n"

def function_exists(fun):
  '''As in PHP, fun is tested as a name, not an object as is common in Python.'''
  try:
    ret = type(eval(str(fun)))
    return ret in (types.FunctionType, types.BuiltinFunctionType)
  except NameError:
    return False
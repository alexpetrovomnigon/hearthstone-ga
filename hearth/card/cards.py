from data.source import Source
from hearth.card.card import Card
#This class represents all available hearthstone cards
class Cards:
    cards = []
    currentStandard = ['EXPERT1', 'GANGS', 'CORE', 'ICECROWN', 'UNGORO', 'KARA', 'LOOTAPALOOZA', 'OG']
    sets = ['TGT', 'HERO_SKINS', 'BRM', 'TB', 'GANGS', 'CREDITS', 'CORE', 'EXPERT1', 'HOF', 'NAXX', 'GVG', 'ICECROWN', 'UNGORO', 'KARA', 'LOE', 'LOOTAPALOOZA', 'OG', 'MISSIONS']
    def __init__(self):
        cards_data = Source().load_data()
        sets = []
        self.cards = []
        for card_data in cards_data[:]:
            keys = list(card_data.keys())
            if "set" in keys:
                if not card_data["set"] in sets:
                    sets.append(card_data["set"])
            card = Card(card_data)
            self.cards.append(card)
    def getSet(self, set):
        set_cards = []
        for card in self.cards[:]:
            if card.set == set:
                set_cards.append(card)
        return set_cards

    def getAllCollectibleCards(self, standard = True):
        required_cards = []
        l = 0
        print(len(self.cards))
        for card in self.cards:
            if card.collectible:
                if standard:
                    if card.set in self.currentStandard:
                        l += 1
                        required_cards.append(card)
                else:
                    l += 1
                    required_cards.append(card)
        return required_cards

    def getAllCardsForClass(self, deck_class, standard = True):
        required_cards = []
        print(len(self.cards))
        for card in self.cards[:]:
            if card.collectible:
                if standard:
                    if card.set in self.currentStandard:
                        if card.cardClass == deck_class or (card.cardClass == "NEUTRAL" and deck_class in card.classes) or (card.cardClass == "NEUTRAL" and not card.classes):
                            required_cards.append(card)
                else:
                    if card.cardClass == deck_class or (card.cardClass == "NEUTRAL" and deck_class in card.classes) or (card.cardClass == "NEUTRAL" and not card.classes):
                        required_cards.append(card)
        return required_cards
    def getById(self, id):
        for card in self.cards[:]:
            if card.dbfId == id:
                return card
        return None
from hearth.card.cards import Cards
from hearth.deck.deck import Deck

import random

class GeneticWorker:
    size = 0
    xProbability = 0
    mProbability = 0
    population = 0
    offsprings = 0
    deck_class = 0
    cards = []
    def __init__(self, deck_class):
        self.size = 50
        self.xProbability = 1
        self.mProbability = 0.01
        self.population = []
        self.offsprings = []
        self.deck_class = deck_class

    def generateInitialPopulation(self):
        self.cards = Cards().getAllCardsForClass(self.deck_class, True)

        while len(self.population) < self.size:
            self.population.append(self.randomDeck())
        return 0
    def caluclateFitness(self):
        for chromosome in self.population:
            chromosome.getFitness()
        self.population.sort(key=lambda x: x._fitness, reverse=True)
    def crossingOver(self):
        pair = 1
        offsprings = []
        while pair <= self.size / 2:
            parents = self.population[pair*2-2:pair*2]
            pair += 1
            offsprings += self.generatingOffsprings(parents)

        self.population += offsprings
        return 0

    def generatingOffsprings(self, parents):
        tries = 0

        while tries < 100:
            point = random.randint(1,29)

            parent1cards = parents[0]._cards
            parent2cards = parents[1]._cards

            offspring1cards = parent1cards[:point] + parent2cards[point:]
            offspring2cards = parent2cards[:point] + parent1cards[point:]

            offspringOne = Deck()
            offspringOne._cards = offspring1cards
            offspringTwo = Deck()
            offspringTwo._cards = offspring2cards

            if offspringOne.isValid() and offspringTwo.isValid():
                return [offspringOne, offspringTwo]

            #shuffling before trying again
            tries += 1
            parent1cards = random.shuffle(parent1cards)
            parent2cards = random.shuffle(parent2cards)
        return []

    def mutation(self):
        for deck in self.population:
            mutated = deck._cards.copy()
            numberOfMutations = 0
            for card in mutated:
                probability = random.uniform(0,1)
                if probability < self.mProbability:
                    numberOfMutations += 1
                    mutated.remove(card)
                    mutated.append(self.randomCard())
            if numberOfMutations > 0:
                mutatedDeck = Deck()
                mutatedDeck._cards = mutated
                if mutatedDeck.isValid():
                    deck._cards = mutated
        return 0
    def selection(self):
        self.caluclateFitness()
        self.population = self.population[:50]
        return 0
    def optimize(self):
        self.generateInitialPopulation()
        for x in range(0,100):
            print("Generation #", x, "\n")
            self.caluclateFitness()
            self.crossingOver()
            self.mutation()
            self.selection()
            print(self.population[0]._fitness)
        self.population[0].printDeck()

    def randomDeck(self):
        isValid = False
        newDeck = None
        while not isValid:
            newDeck = Deck()
            while newDeck.getSize() < 30:
                newDeck.addCard(self.randomCard())
            isValid = newDeck.isValid()
        return newDeck

    def randomCard(self):
        return random.choice(self.cards)


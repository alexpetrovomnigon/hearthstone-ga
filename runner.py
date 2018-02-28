from genetic.worker import GeneticWorker
from hearth.card.cards import Cards

#worker = GeneticWorker("WARRIOR")

#worker.optimize()

cards = Cards().getAllCollectibleCards(True)

print(len(cards))
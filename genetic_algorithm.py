import operator
import random
import numpy as np

class GA(object):

    def __init__(self, populationSize, numberOfGenes, crossoverProbability, mutationProbability,
                 selectionMethod, tournamentSelectionParameter, tournamentSize, numberOfVariables,
                 variableRange, numberOfGenerations, useElitism, numberOfBestIndividualCopies, fitnessFunction):

        self.populationSize = int(populationSize)
        self.numberOfGenes = int(numberOfGenes)
        self.crossoverProbability = float(crossoverProbability)
        self.mutationProbability = float(mutationProbability)
        self.selectionMethod = int(selectionMethod)
        self.tournamentSelectionParameter = float(tournamentSelectionParameter)
        self.tournamentSize = int(tournamentSize)
        self.numberOfVariables = int(numberOfVariables)
        self.variableRange = variableRange
        self.numberOfGenerations = int(numberOfGenerations)
        self.useElitism = bool(useElitism)
        self.numberOfBestIndividualCopies = int(numberOfBestIndividualCopies)
        self.fitness = np.zeros((populationSize,1))
        self.normalizedFitness = np.zeros((populationSize,1))
        self.population = self.InitializePopulation(populationSize, numberOfGenes)
        self.vars = np.zeros((populationSize,numberOfVariables))
        self.data = np.zeros((populationSize,numberOfVariables+1))
        self.generation = 0
        self.EvaluateIndividual = fitnessFunction
        self.CalculateFitness()

    def CalculateFitness(self):
        self.maximumFitness = float("-inf")
        self.minimumFitness = float("inf")
        self.totalFitness = 0.0
        self.averageFitness = 0.0
        self.totalNormalizedFitness = 0.0
        self.averageNormalizedFitness = 0.0

        for i in range(self.populationSize):
            chromosome = self.population[i]
            self.vars[i] = self.DecodeChromosome(chromosome, self.numberOfVariables, self.variableRange)
            self.fitness[i][0] = self.EvaluateIndividual(self.vars[i])
            self.totalFitness = self.totalFitness + self.fitness[i][0]
            if self.fitness[i][0] > self.maximumFitness:
                self.maximumFitness = self.fitness[i][0]
                self.bestIndividualIndex = i
            if self.fitness[i][0] < self.minimumFitness:
                self.minimumFitness = self.fitness[i][0]
            self.data[i][0:self.numberOfVariables] = self.vars[i]
            self.data[i][self.numberOfVariables] = self.fitness[i][0]
        self.averageFitness = self.totalFitness / float(self.populationSize)

        fitnessRange = self.maximumFitness - self.minimumFitness
        if(fitnessRange == 0): fitnessRange = 0.01
        for i in range(self.populationSize):
            self.normalizedFitness[i][0] = (self.fitness[i][0] - self.minimumFitness) / float(fitnessRange)
            self.totalNormalizedFitness = self.totalNormalizedFitness + self.normalizedFitness[i][0]
        self.averageNormalizedFitness = self.totalNormalizedFitness / float(self.populationSize)

    def InitializePopulation(self, populationSize, numberOfGenes):
        population = np.random.random_integers(0,1,(populationSize,numberOfGenes))
        return population

    def DecodeChromosome(self, chromosome, nVariables, variableRange):
        nGenes = np.size(chromosome,0) # Number of genes in the chromosome
        nBits = nGenes/nVariables      # Number of bits (genes) per variable

        vars = np.zeros(nVariables)    # Create a one-dimensional Numpy array of variables

        # Calculate the value of each variable from the bits in the bit string
        ##############################
        ### YOU'RE CODE GOES HERE ####
        ##############################


        genes = 0
        length = 0
        for i in range(vars.size):
            lower = variableRange[i][0]
            upper = variableRange[i][1]
            power = -1
            value = 0

            for bit in range(nBits):
                sum = pow(2, power)
                value += sum * chromosome[bit+genes]
                power -= 1

        length += 1
        genes = length * nBits
        vars[i] = lower + (upper - lower) / (1 - pow(2, -nBits)) * value

        return vars

    def RouletteWheelSelect(self, normalizedFitness):
        selected = 0

        # Use Roulette-Wheel Selection to select an individual to the mating pool
		##############################
        ### YOU'RE CODE GOES HERE ####
        ##############################
        for i in range(len(normalizedFitness)):
            selected += normalizedFitness[i]
        r = random.random()
        for x in range(len(normalizedFitness)):
            sum += (normalizedFitness[i] / selected)
            if sum >= r:
                return i 
        return selected

    def TournamentSelect(self, fitness, tournamentSelectionParameter, tournamentSize):
        selected = 0

		# Use Tournament Selection to select an individual to the mating pool
		
        ##############################
        ### YOU'RE CODE GOES HERE ####
        ##############################
        fitnessList = []

        for i in range(tournamentSize):
            fitnessList.append(random.randint(0, len(fitness)-1))

        while len(fitnessList) > 1:
            A = fitnessList.pop()
            B = fitnessList.pop()
            if fitness[A] > fitness[B]:
                if random.random() < tournamentSelectionParameter:
                    fitnessList.append(A)
                else:
                    fitnessList.append(B)
            else:
                if random.random() < tournamentSelectionParameter:
                    fitnessList.append(B)
                else:
                    fitnessList.append(A)

        selected = fitnessList.pop()
        return selected

    def Cross(self, chromosome1, chromosome2, crossoverProbability):

		# Cross the two individuals "in-place"
		# NB! Don't forget to use the crossover probability
		
        ##############################
        ### YOU'RE CODE GOES HERE ####
        ##############################
        if random.random() <= crossoverProbability:
            crossOver = random.randint(0, (np.size(chromosome1) - 1))

            temp = chromosome1[:crossOver].copy()
            chromosome1[:crossOver] = chromosome2[:crossOver].copy()
            chromosome2[:crossOver] = temp.copy()

    def Mutate(self, chromosome, mutationProbability):

        for i in range(len(chromosome)):
            if random.random() <= mutationProbability:
                if chromosome[i] == 1:
                    chromosome[i] = 0
                else:
                    chromosome[i] = 1

        # Mutate the individuals "in-place"
		# NB! Don't forget to apply the mutation probability to each bit
		
		##############################
        ### YOU'RE CODE GOES HERE ####
        ##############################

    def InsertBestIndividual(self, population, individual, numberOfBestIndividualCopies):
        for i in range(numberOfBestIndividualCopies):
            population[-1-i] = individual.copy()

    def Step(self):
        if self.populationSize % 2 == 0:
            tempPopulation = np.zeros([self.populationSize,self.numberOfGenes], dtype=int)
        else:
            tempPopulation = np.zeros([self.populationSize+1,self.numberOfGenes], dtype=int)

        for i in range(0,self.populationSize,2):
            if self.selectionMethod == 0:
                i1 = self.TournamentSelect(self.fitness,self.tournamentSelectionParameter,self.tournamentSize)
                i2 = self.TournamentSelect(self.fitness,self.tournamentSelectionParameter,self.tournamentSize)
            else:
                i1 = self.RouletteWheelSelect(self.normalizedFitness)
                i2 = self.RouletteWheelSelect(self.normalizedFitness)
            chromosome1 = self.population[i1].copy()
            chromosome2 = self.population[i2].copy()

            self.Cross(chromosome1,chromosome2,self.crossoverProbability)
            self.Mutate(chromosome1,self.mutationProbability)
            self.Mutate(chromosome2,self.mutationProbability)

            tempPopulation[i] = chromosome1
            tempPopulation[i+1] = chromosome2

        if self.populationSize % 2 != 0:
            tempPopulation = tempPopulation[0:self.populationSize]

        if self.useElitism:
            bestIndividual = self.population[self.bestIndividualIndex]
            self.InsertBestIndividual(tempPopulation,bestIndividual,self.numberOfBestIndividualCopies)
        self.population = tempPopulation
        self.generation += 1
        self.CalculateFitness()

    def Run(self):
        while self.generation < self.numberOfGenerations:
            self.Step()

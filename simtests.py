import random, sys
random.seed(42)
from person import Person
from simulation import Simulation
from virus import Virus

virus = Virus("Ebola", .5, .7)
sim = Simulation(100000, .08, 10, virus)

def test_create_population():

    sim._create_population()
    assert len(sim.population) == sim.population_size
    infected_count_test = 0
    vaccination_count_test = 0
    for person in sim.population:
        if person.is_infected == True:
            infected_count_test +=1
    for person in sim.population:
        if person.is_vaccinated:
            vaccination_count_test +=1
    assert infected_count_test == sim.initial_infected
    # checks if vaccinated percentaion is within 10% of vacc percentage rate
    vacc_percentage =  float(vaccination_count_test)/ sim.population_size
    assert vacc_percentage >= sim.vaccination_percentage - .1
    assert vacc_percentage <= sim.vaccination_percentage + .1

def test_infect_the_weak():
## checking if people are getting infected  -- subtracts one from ID because person._id starts at 1 while the index in population list starts at 0
    sim._create_population()
    sim.newly_infected = [200]
    person1 = sim.population[199]
    assert person1.is_infected == False
    sim.infect_the_weak()
    person1 = sim.population[199]
    assert person1.is_infected == True

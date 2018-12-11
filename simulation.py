import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):


    def __init__(self, population_size, vaccination_percentage, initial_infected, virus = None):

        self.population = [] # List of Person objects
        self.population_size = (population_size)

        self.next_person_id = 0 # Int

        self.initial_infected = (initial_infected) # Int
        self.total_infected = 0 # Int
        self.vaccination_percentage = (vaccination_percentage) # float between 0 and 1

        self.vacc_int = 0

        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus.name, population_size, vaccination_percentage, initial_infected)
        self.newly_infected = []

        self.logger = Logger(self.file_name)
        self.logger.write_metadata(self.population_size, self.vaccination_percentage, virus.name, virus.mortality_rate, virus.repro_rate)

    def _create_population(self):
        infected_count = 0
        while len(self.population) < self.population_size:
            id = len(self.population) + 1
            if infected_count < self.initial_infected:

                new_person = Person(id, False, True, virus)
                self.total_infected += 1
                infected_count +=1
                self.population.append(new_person)
            else:
                if random.random() > self.vaccination_percentage:
                    new_person = Person(id, False, False, virus)
                    self.population.append(new_person)
                else:
                    new_person = Person(id, True, False, virus)
                    self.population.append(new_person)


    def _simulation_should_continue(self):
        for person in self.population:
            if person.is_infected == True:
                return True
        return False
        # TODO check the else return value


    def run(self):
        self._create_population()
        should_continue = self._simulation_should_continue()
        step_counter = 0
        while should_continue == True:
            self.time_step()
            step_counter += 1
            should_continue = self._simulation_should_continue()

        print("The simulation has ended after", step_counter, " turns.")
        print("Total infected", self.total_infected, "Total Dead", self.total_dead)
        print("Interactions where indidual as safe from vacciation", self.vacc_int)

        self.logger.log_time_step(self.total_dead, step_counter)


    def time_step(self):
        for person in self.population:
            if person.is_alive == True and person.is_infected== True:
                i = 0
                while i < 5:
                    random_person = self.population[random.randint(0, self.population_size - 1)]
                    if random_person.is_alive == True:
                        self.interaction(person, random_person)
                        i += 1
        self.kill_the_weak()
        self.infect_the_weak()


    # def log_interaction(self, person, random_person, random_person_sick, random_person_vacc, did_infect):

    def interaction(self, person, random_person):
        # if random.random() < virus.repro_rate and random_person.is_vaccinated == False and random_person.is_infected == False:
        if random.random() <= virus.repro_rate and random_person.is_vaccinated == False:
            if random_person.is_infected == False:
                self.total_infected +=1
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, random_person.is_infected, random_person.is_vaccinated, True)
            else:
                self.logger.log_interaction(person, random_person, random_person.is_infected, random_person.is_vaccinated, True)
        else:
            self.vacc_int +=1
            self.logger.log_interaction(person, random_person, random_person.is_infected, random_person.is_vaccinated, False)

    def infect_the_weak(self):
        if len(self.newly_infected) > 0:
            for id in self.newly_infected:
                newid = id-1
                person = self.population[newid]
                person.is_infected = True
        self.newly_infected = []




    # def log_infection_survival(self, person, did_die_from_infection):

    def kill_the_weak(self):
        for person in self.population:
            if person.is_infected == True:
                if person.did_survive_infection() == True:
                    # he ded
                    self.logger.log_infection_survival(person, False)
                else:
                    # he not ded
                    self.logger.log_infection_survival(person, True)
                    self.total_dead += 1

    ##TODO L@@K

    def printlist(self):
        for person in self.population:
            print(person._id, "Alive", person.is_alive, "Vac", person.is_vaccinated, "Inf", person.is_infected)

population_size = 100000
vaccination_percentage = .8
initial_infected = 10

# virus_name = "ebola"
# mortality_rate = .5
# basic_repro_num= .5
# def __init__(self, name, repro_rate, mortality_rate):

# virus = Virus("Ebola", .5, .7)


# sim = Simulation(population_size, vaccination_percentage, initial_infected, virus)
# sim._create_population()
# sim.printlist()
# sim.time_step()
# sim.printlist()
# sim.run()

if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)
    sim.run()
#


def test_create_population():
    # virus = Virus('testvirus', .25, .25)
    # sim = Simulation(100000, .07, 10, virus)
    # create some people to test if our init method works as expected
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

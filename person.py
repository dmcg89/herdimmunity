from virus import Virus
import random
random.seed(42)


class Person(object):

    def __init__(self, _id, is_vaccinated=None, is_infected=None, infection=None):

        self._id = _id  # int
        self.is_alive = True  # boolean
        self.is_vaccinated = is_vaccinated  # boolean
        self.infection = infection  # Virus object or None
        self.is_infected = is_infected

    def did_survive_infection(self):

        if random.random() >= self.infection.mortality_rate:
            # Survives
            self.is_infected = False
            self.is_vaccinated = True
            return True

        else:
            #dies
            self.is_infected = False
            self.is_alive = False
            return False

''' These are simple tests to ensure that you are instantiating your Person class correctly. '''
def test_vacc_person_instantiation():
    # create some people to test if our init method works as expected
    person = Person(1, True)
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False, True)
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.is_infected is True


def test_sick_person_instantiation():
    # Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
    # Create a Person object and give them the virus infection
    person = Person(3, False, None, virus)
    # assert infection.name == "Dysentery"
    # assert infection.repro_rate == .7
    # assert infection.mortality_rate == .2
    assert person.infection == virus

#PERSON
# def __init__(self, _id, is_vaccinated=None, is_infected=None, infection=None):
#VIRUS
# def __init__(self, name, repro_rate, mortality_rate):

def test_did_survive_infection():
    # TODO: Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
    # TODO: Create a Person object and give them the virus infection
    person = Person(4, False, True, virus)
    print("here")
    # Resolve whether the Person survives the infection or not
    survived = person.did_survive_infection()
    # Check if the Person survived or not
    if survived:
        assert person.is_alive is True
        # TODO: Write your own assert statements that test
        # the values of each attribute for a Person who survived
        # assert ...
        assert person.is_vaccinated is True
        assert person.is_infected is False
        print('here1')
    else:
        assert person.is_alive is False
        # TODO: Write your own assert statements that test
        # the values of each attribute for a Person who did not survive
        # assert ...
        assert person.is_vaccinated is False
        assert person.is_infected is False
        print('here2')

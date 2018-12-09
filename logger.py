class Logger(object):


    def __init__(self, file_name):

        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        self.file = open(self.file_name, "w+")
        self.file.write(
            "Population Size: {}\tVaccination Percentage: {}\tVirus Name: {}\tMortality Rate: {}\tReproduction: {}\n".format(
                pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num))
        self.file.close()


    def log_interaction(self, person, random_person, random_person_sick,
                        random_person_vacc, did_infect):
        self.file = open(self.file_name, "a")
        self.file.write(
            # "Interaction between patient {} and citizen {}\nCitizen {} Vaccinated: {}\n".format(person._id, random_person._id, random_person._id, random_person.is_vaccinated))
            "Interaction between patient {} and citizen {}\nCitizen {} Vaccinated: {}\n Citizen {} Sick: {}\n".format(person._id, random_person._id, random_person._id, random_person.is_vaccinated, random_person._id, random_person_sick,))


        if did_infect == True:
            self.file.write("Citizen {} is now sick\n".format(random_person._id))

        self.file.close()

    def log_infection_survival(self, person, did_die_from_infection):
        self.file = open(self.file_name, "a")
        if did_die_from_infection == True:
            self.file.write("Patient {} was killed from infection\n".format(person._id))
        else:
            self.file.write("Patient {} survived the infection\n".format(person._id))
        self.file.close()

    def log_time_step(self, total_dead, counter):
        self.file = open(self.file_name, "a")
        self.file.write("Total Deaths: {}\nNumber of Weeks: {}".format(total_dead, counter))

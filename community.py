import yaml
import random
import person

config = yaml.safe_load(open('config.yml'))


class Community:
    """
    Creates a list of people, their characteristics, and their relationships
    """

    """set values"""
    pop = config["community"]["prime_population"]
    relate_intense = config["community"]["relationship_intensity"]
    community = []

    def __init__(self):
        self.load_pop()

    """ get initial population """
    def load_pop(self):
        for person_number in range(self.pop):
            self.community.append(person.Person())

    """ get relations """
    for p in community:
        no_of_relatives = range(random.randint(*config["community"]["family_size_range"]))
        for no in no_of_relatives:
            community.append(p.create_relation())

    """ print population """
    def __repr__(self):
        retstr = ''
        for i in range(self.pop):
            retstr += f"{self.community[i]}\n"
        return retstr


community = Community()
print(len(community.community))
print(f"{str(community)}")
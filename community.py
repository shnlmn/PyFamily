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
        # self.load_pop()
        self.Person = person.Person

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
            print(f"index {i} - {self.community}")
            retstr += f"{self.community[i]}\n"
        return retstr

    def generate(self):
        self.community = []
        count = 0
        num_relatives = random.randint(*config["community"]["family_size_range"])
        print(num_relatives)
        while count < num_relatives:
            if len(self.community) == 0:
                self.community.append(self.Person())
                count += 1
                if self.community[0].req_relative == True:
                    self.community.append(self.community[0].create_relation())
                    count +=1
            else:
                self.community.append(self.community[-1].create_relation())
                count += 1
        for c in self.community:
            c.check_relations(self.community)
            print(f"{c.full_name} is a {c.sex} in {c.pronouns[2]} {c.age_range} at {c.age}")
            for r in c.relations:
                print(f"{r.first_name} is {c.pronouns[2]} {c.relations[r]}. ")
        return self.community


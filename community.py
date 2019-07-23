import yaml
import random
import person
from colors import *

config = yaml.safe_load(open('config.yml'))

class Community:
    """
    Creates a list of people, their characteristics, and their relationships
    """

    """set values"""
    pop = config["community"]["prime_population"]
    relate_intense = config["community"]["relationship_intensity"]
    number_of_children = config['community']['child_number_range']
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

    def create_color(self, age_range, relation):
        color_dict = dict(list(zip(
            config['age_ranges'],
            list(css_colors.keys())
        )))
        relation_dict = dict(list(zip(
            list(config['community']['family_relation']),list(css_colors.keys())
        )))
        return color_dict[age_range], relation_dict[relation]

    def spouse_sex(self, i):
        sexes = ['male', 'female']
        sexes.remove(i.sex)
        return sexes[0]

    def generate(self):
        self.community = []
        count = 0
        #num_relatives = random.randint(*config["community"]["family_size_range"])
        # print(num_relatives)

        prime = person.Person(age_range=random.choice(["70s", "60s"]))
        self.community.append(prime)
        self.community.append(prime.create_relation(relation='spouse', sex=self.spouse_sex(prime)))

        for n in range(*self.number_of_children):

            parent = self.community[0].create_relation(relation='child')
            self.community.append(parent.create_relation(relation="spouse", sex=self.spouse_sex(parent)))

            if parent.age_range not in ['child', 'teen']:
                for t in range(*self.number_of_children):
                    child = parent.create_relation(relation='child')

                    if child.age_range not in ['child', 'teen']:

                        self.community.append(child.create_relation(relation="spouse", sex=self.spouse_sex(child)))
                        for e in range(*self.number_of_children):
                            grandchild = child.create_relation(relation='child')

                            self.community.append(grandchild)

                    self.community.append(child)

            self.community.append(parent)

        self.community = sorted(self.community, key=lambda x: x.age)
        for c in self.community:
            c.check_relations(self.community)
        for c in self.community:
            c.check_relations(self.community)

        return self.community


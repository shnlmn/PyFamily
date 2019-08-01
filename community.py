import yaml
import random
import person
from colors import *
import colorsys

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
        self.relation_color = self.set_relation_colors()
        self.age_range_keys = list(config["age_ranges"].keys())

    """ get a dict of RGB colors for all the different relations """
    def set_relation_colors(self):
        color_dict = {}
        for i,rel in enumerate( person.relation_def.keys() ):
            hue = i/len(person.relation_def.keys())
            rgb = colorsys.hsv_to_rgb(hue, 1, 1)
            rgb = [int(x*255) for x in rgb]
            hex = ''.join(['{:02X}'.format(int(round(x)))for x in rgb])
            print(hex)
            color_dict.update({rel:hex})

        return color_dict

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

        '''Time is a flat circle
        Create a person, age them incrementally while randomly adjusting their personality
        When they reach maturity, they can pick up a mate and child
        They may also move on to another mate, have more children, or be single'''

        self.community = []
        self.community.append(person.Person(age_range='child'))
        decade = 0
        generations = 4 # stop after the youngest of 4 generations have matured
        generation = 0
        while generation <= generations:
            for individual in self.community:
                if individual.alive:
                    for k, v in individual.personality:
                        individual.personality[k] = v*random.random()*10
                    try:
                        individual.age_range = self.age_range_keys[
                            self.age_range_keys.index.(individual.age_range)+1]]
                    except ValueError:
                        print(f"{individual.full_name} has died.")
                        individual.alive = False
        count = 0
        # num_relatives = random.randint(*config["community"]["family_size_range"])
        # print(num_relatives)

        prime = person.Person(age_range=random.choice(["70s", "60s"]))
        self.community.append(prime)
        self.community.append(prime.create_relation(relation='spouse', sex=self.spouse_sex(prime)))
        # youngest = sorted([prime, prime.relations['spouse']], key=lambda _: _.age)[0]
        print(f"I am {prime.full_name}, my spouse is {prime.find_relation('spouse')[0].full_name}")
        youngest = sorted([prime, prime.find_relation("spouse")[0]], key = lambda _: _.age)[0]

        for n in range(*self.number_of_children):

            parent = youngest
            if parent.age_range not in ['child', 'teen']:
                for t in range(*self.number_of_children):
                    child = parent.create_relation(relation='child')

                    if child.age_range not in ['child', 'teen']:

                        self.community.append(child.create_relation(relation="spouse", sex=self.spouse_sex(child)))
                        youngest = sorted([child, child.find_relation('spouse')[0]], key=lambda _: _.age)[0]

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


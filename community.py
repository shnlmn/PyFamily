import yaml
import random
import person
from collections import OrderedDict
from termcolor import colored, cprint
import termcolor

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

    def create_color(self, age_range, relation):
        color_dict = dict(list(zip(
            config['age_ranges'],
            list(termcolor.COLORS.keys())
        )))
        relation_dict = dict(list(zip(
            config['relations']
        )))
        return color_dict[age_range]

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
        # foo = OrderedDict(sorted(foo.iteritems(), key=lambda x: x[1]['depth']))

        for c in self.community:
            c.check_relations(self.community)

        for i, c in enumerate(self.community):
            if i == 0:
                cprint(f"{c.first_name} is {c.age} and is ",
                       color = self.create_color(c.age_range),
                       end='')
            elif i < len(self.community)-1:
                cprint(f"{c.first_name}'s ({c.age}) {c.relations[self.community[i-1]]}, who is ",
                      color = self.create_color(c.age_range),
                      end='')
            else:
                cprint(f"{c.first_name}'s ({c.age}) {c.relations[self.community[i-1]]}.",
                      color = self.create_color(c.age_range) )

        self.community = sorted(self.community, key=lambda x: x.age, reverse=True)

        for c in self.community:
            c.relations = OrderedDict(sorted(c.relations.items(), key=lambda x: x[0].age, reverse=True))
            cprint(f"\n\n{c.full_name} is a {c.sex} in {c.pronouns[2]} {c.age_range} at {c.age}",
                   color = self.create_color(c.age_range))
            for r in c.relations:
                cprint(f"{r.first_name:>10} | {r.age:^4} | {c.relations[r]:<12} ",
                       color = self.create_color(r.age_range),
                       end='')
        return self.community


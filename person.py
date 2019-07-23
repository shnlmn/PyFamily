import yaml
import random
import names
import pandas
from collections import OrderedDict

config = yaml.safe_load(open("config.yml"))
with open(config['paths']['FRC']) as csvfile:
    relation_def = pandas.read_csv(csvfile, header = 0, index_col = 0)
'''
Person is created
they are given arbitrary parameters
they are given a random number of relatives
from that number, more people are created:
    each person is given a relation based on 1) a need for a required relative (parent to child, eg.) or 
    2) a total list of likely relatives
    Based on the relation, the new person is given an age range and age
'''
# TODO - Bloodline style. 4 generations are created of one bloodline. Grandparents propogate children,
#  who have children, who have children.
#   Then a time is established to give everyone an age.
#   Each person who generates a child also generates a mate of opposite gender.
#   Then, each person decides if they are married to their mate, single, or married to someone other than the mate.
#   Each person outside of the bloodline is gen'd a small family (parent, sibling, children from another mate).
#   These may appear in the story.

class Person:
    global relation_def
    def __init__(self , age_range = '', last_name = '', sex = ''):
        self.relation_def = relation_def
        self.relations = OrderedDict() # this dict pattern will be {Person<class>: <str>relation}
        self.age_range = age_range
        self.age_ranges = config['age_ranges']
        self.age_range_keys = list(config["age_ranges"].keys())
        self.set_age()
        self.sex, self.pronouns = self.set_sex(sex)

        self.last_name = names.get_last_name() if last_name is '' else last_name
        self.first_name = names.get_first_name(self.sex)
        self.full_name = self.first_name + " " + self.last_name

        self.allowed_relatives = config["age_relatives"][self.age_range]
        self.all_allowed_relatives = self.allowed_relatives["required"]+self.allowed_relatives["other"]
        self.req_list = self.allowed_relatives["required"]
        self.req_relative = True if self.req_list and len(self.relations) == 0 else False


    def clamp(self,n, minn, maxn):
        return max(min(maxn, n), minn)

    def __repr__(self):
        return (f"{self.full_name} is a {self.age_range} at {self.age}. They are a {self.sex}\n" \
               f"{[[x.full_name, self.relations[x]] for x in self.relations]}")

    # Class Method
    def create_relation(self, relation='', sex=''):
        # TODO check if individual has more than two parents.
        #  Either limit parents to two, create spouse/exspouse/step-parent or allow bigamy.
        cls = type(self)
        if relation:
            relation_data = self.get_relation_data(relation)
        elif self.req_list:
            relation_data = self.get_relation_data(self.req_list)
        else:
            relation_data = self.get_relation_data(self.all_allowed_relatives)
        # print(f"RelationData {relation_data}")
        new_person = cls(relation_data[0], self.last_name, sex)
        self.relations = {new_person: relation_data[1]}
        new_person.relations.update({self: self.relation_def[self.relations[new_person]]['me']})
        self.req_relative = False
        return new_person

    def get_relation_data(self,relation_type):
        if relation_type:
            relative = relation_type
        else:
            relative = random.choice(relation_type)
        age_diff = config["relative_params"][relation_type]["age_diff"]
        # print(f"relative: {relative}. Random age diff: {age_diff}")
        relation_age_index = self.clamp(self.age_range_keys.index(self.age_range)+random.randint(*age_diff), 0, len(self.age_ranges)-1)
        relation_age_range = self.age_range_keys[relation_age_index]
        # print(f"Their {relative}'s age range is: { relation_age_range }")
        return relation_age_range, relative

    def check_relations (self, others):
        # Families are intertwined
        # If you are my  ____ : Then your ___ is my ____
        for other in others:
            if other is not self and other in self.relations:  # ignore yourself and make sure you are in the relations
                for others_relation, others_relation_type in other.relations.items():  # go through current family members relations
                    if others_relation not in self.relations and others_relation is not self:  # ignore relations already known and yourself
                        self.relations.update(
                            {others_relation:
                                self.split_relation(
                                    self.relation_def[self.relations[other]][other.relations[others_relation]]
                                    # bob               bob    Tina   parent  Tina      joan      cousin
                                )
                            })
                        others_relation.relations.update(
                            {self:
                                self.split_relation(
                                    self.relation_def[self.relations[others_relation]]['me']
                                )
                            }
                        )

    def set_age(self):
        if self.age_range is '':
            self.age_range = random.choice(list(self.age_ranges))
            self.age = random.choice(range(*self.age_ranges[self.age_range]))
        else:
            self.age = random.choice(range(*self.age_ranges[self.age_range]))
        # print(f"My age is {self.age}.")

    def split_relation(self, relation):
        if ":" in relation:
            print("GOT SPLIT")
            return(random.choice(relation.split(":")).strip())
        else:
            return(relation)

    def set_sex(self, sex_choice = ''):
        if sex_choice in ("male", "female"):
            sex = sex_choice
        else:
            sex = random.choice(["male", "female"])
        if sex is "male":
            pronouns = ["he", "him", "his"]
        else:
            pronouns = ["she", "her", "her"]
        return(sex, pronouns)

if __name__ == "__main__":
    community = []
    count = 0
    num_relatives = random.randint(*config["community"]["family_size_range"])
    print(num_relatives)
    while count < num_relatives:
        relation_gen = None
        if len(community) == 0:
            community.append(Person()) # create the initial family member
            count += 1
            print(community[0])
            if community[0].req_relative:
                relation_gen = community[0].create_relation()
                community.append(relation_gen)
                count +=1
                print(relation_gen)
        else:
            relation_gen = community[-1].create_relation()
            community.append(relation_gen)
            count += 1
            print(relation_gen)
    for c in community:
        c.check_relations(community)
        print(f"{c.full_name} is a {c.sex} in {c.pronouns[2]} {c.age_range} at {c.age}")
        for r in c.relations:
            print(f"{r.first_name:15} | {c.relations[r]}. ")


import community
from collections import OrderedDict
import random

past_seed = None
seed = None
if __name__ == "__main__":
    while True:

        print("\nEnter a value for the seed: ", end='')

        if past_seed:
            print(f"({past_seed})")

        seed = input('')

        if seed is '':
            if past_seed:
                seed = past_seed
            else:
                print("No seed was provided. Using random seed")
                seed = random.randint(0,100000000)
                print(seed)
        try:
            seed = int(seed)
        except(ValueError):
            print("Please enter an integer")
            seed = past_seed
            continue


        random.seed(a=seed)
        commune = community.Community().generate()
        past_seed = seed
        seed = None

        for i, c in enumerate(commune):
            if i == 0:
                print(f"{c.first_name} is {c.age} and is " ,end='')
            elif i < len(commune)-1:
                print(f"{c.first_name}'s ({c.age}) {c.relations[commune[i-1]]}, who is ",end='')
            else:
                print(f"{c.first_name}'s ({c.age}) {c.relations[commune[i-1]]}.")

        commune = sorted(commune, key=lambda x: x.age, reverse=True)
        for c in commune:
            c.relations = OrderedDict(sorted(c.relations.items(), key=lambda x: x[0].age, reverse=True))

            print(f"\n\n{c.full_name} is a {c.sex} in {c.pronouns[2]} {c.age_range} at {c.age}")

            for r in c.relations:

                print(f"{r.first_name:>10} | {r.age:^4} | {c.relations[r]:<12} ",end='')

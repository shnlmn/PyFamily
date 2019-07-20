import community
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
        commune = community.Community()
        commune.generate()
        past_seed = seed
        seed = None

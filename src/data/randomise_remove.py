import os
import random

# change current directory to maain directory
os.chdir("../")
os.chdir("../")

no_of_yes_instances = len([name for name in os.listdir("./data/yes/") if os.path.isfile("./data/yes/" + name)])
no_of_no_instances = len([name for name in os.listdir("./data/no/") if os.path.isfile("./data/no/" + name)])

print(f"Number of 'yes' instances: {no_of_yes_instances}")
print(f"Number of 'no' instances:  {no_of_no_instances}")

difference = abs(no_of_no_instances - no_of_yes_instances)

print("=================================")
print(f"Difference:                {difference}")

print(f"Getting {difference} numbers of 'no' instances")
differences_set = set()
while (len(differences_set) != difference):
    rand_int = random.randint(no_of_yes_instances, no_of_yes_instances + no_of_no_instances - 1)
    differences_set.add(rand_int)

print(f"Removing {difference} instances in 'no' dataset")
for audio_no in differences_set:
    os.remove(f"./data/no/{audio_no}.wav")

no_of_yes_instances = len([name for name in os.listdir("./data/yes/") if os.path.isfile("./data/yes/" + name)])
no_of_no_instances = len([name for name in os.listdir("./data/no/") if os.path.isfile("./data/no/" + name)])

print(f"Number of 'yes' instances: {no_of_yes_instances}")
print(f"Number of 'no' instances:  {no_of_no_instances}")

file = open("{}.txt".format(input("Enter file name: ")), 'w')

import random
numpatients = random.randint(20,40)
numhosptials = random.randint(7,15)
file.write("{}\n".format(numpatients))
file.write("{}\n".format(numhosptials))
emergencies = ['b','l','k','h']
for i in range(numpatients-1):
    file.write("{},".format(random.choice(emergencies)))
file.write("{}\n".format(random.choice(emergencies)))

for i in range(numpatients-1):
    random.shuffle(emergencies)
    file.write("{},".format("".join(emergencies)))
random.shuffle(emergencies)
file.write("{}\n".format("".join(emergencies)))

for i in range(numpatients):
    for j in range(numhosptials-1):
        file.write("{},".format(random.randint(1,20)))
    file.write("{}\n".format(random.randint(1,20)))
    
file.close()
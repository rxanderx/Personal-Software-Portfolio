import random

on = True
random_number = random.randint(0, 10000000)

if random_number != 1337:
    print("Hello World")
else:
    print("This arbitrary chance result is very lucky (or unlucky!) depending on how you view it. Please rerun the code to see the correct output.")

import random
num = random.randint(1,100)
status = 2
def guess():
    print("Guess a number between 1 and 100")
    global status
    while status != 1:
        number = input(int)
        if int(number) == int(num):
            print("Correct!")
            status = 1
        else:
            if int(number) <= int(num):
                print("Too low!")
                guess()
            if int(number) >= int(num):
                print("Too high!")
                guess()
            status = 0
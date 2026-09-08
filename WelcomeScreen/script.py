import random
secret = random.randint(1, 100)
guess = int(input("What MAGIC number am I thinking of? "))

while guess != secret:

    if abs(guess - secret) == 1 or abs(guess - secret) == 2:
        if guess < secret:
            print(f"Super close! Go up by {secret - guess}.")
        else:
            print(f"Super close! Go down by {guess - secret}.")

    guess = int(input("Don't stop now, keep going!"))

print("Are you sure you're not a magican?")
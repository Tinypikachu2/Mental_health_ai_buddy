#TashaWasHere
toons = ["Spongebob", "Patrick", "Squidward", "Sandy", "Mr. Krabs", "Gary"]

for toon in toons:
    SB = input("Which Spongebob character are you more like? ")
    print("Congratulations, you are:", SB, toon)
    play_again = input("Would you like to play again? Y/N ")
    if play_again.upper() == "N":
        break

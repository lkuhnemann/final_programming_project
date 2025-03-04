import json #save + load data about the pet
import time #helps when stats should decrease over time

#make a list of available pets to choose from
pet_types = ["Dog", "Cat", "Rabbit", "Hamster", "Fox", "Guinea Pig"]

# make the default statistics for the pet
pet = {
    "Name": "", #chosen by the user
    "Type": "", #chosen by the user
    "Hunger": 50, #starts at 50 (higher is worse)
    "Happiness": 50, #starts at 50 (higher is better)
    "Health": 50, #starts at 50 (higher is better but drops over time)
    "Last updated": time.time(), #tracks the time for the statistics to decrease
    "Alive": True #if False, the pet has died
}

# save the game process to a JSON file so the user can continue playing later
def save_game():
    with open("pet_data.json", "w") as f:
        json.dump(pet, f)
    print("✅ Game saved!")

# loading a saved (existing) game, if no save is found, it starts a new game
def load_game():
    global pet
    try:
        with open("pet_data.json", "r") as f:
            pet = json.load(f)
        print(f"🎉 Welcome back! {pet['name']} the {pet['type']} is waiting for you")
    except FileNotFoundError:
        print("⚠️ No saved game found. Let's create a new pet for you to take care of!")
        create_pet()


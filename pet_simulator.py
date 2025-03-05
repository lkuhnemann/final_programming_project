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
    "Last_updated": time.time(), #tracks the time for the statistics to decrease
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

# Create a new pet and let the user choose its type (and making sure it is valid)
def create_pet():
    pet["name"] = input("🐾 Enter a name for your pet ").capitalize()
    while True:
        pet_type = input(f"Choose a pet type {pet_types}: ").capitalize()
        if pet_type in pet_types:
            pet["type"] = pet_type
            break
        print("⚠️ Your choice is invalid, please choose a valid pet type")
    print(f"🎉 You adopted {pet['name']} the {pet['type']}! Make sure you take good care of them!")

# Updating the pets statistics over time
def update_statistics():
    if not pet["Alive"]:
        return

    time_passed = time.time() - pet["last updated"]
    decay_amount = int(time_passed // 10) # every 10 seconds the statistics decay
    if decay_amount > 0:
        pet["Hunger"] = min(100, pet["Hunger"] + decay_amount)
        pet["Happiness"] = max(0, pet["Happiness"] - decay_amount)
        pet["Health"] = max(0, pet["Health"] - decay_amount // 2)
        pet["Last_updated"] = time.time()

        if pet["Hunger"] >= 100 or pet["Health"] <= 0: # if hunger reaches 100 or health reaches 0, the pet dies
            pet["Alive"] =False
            print(f"💀 {pet['name']} has died... You did not take proper care of them")


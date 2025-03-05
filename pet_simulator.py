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

# Feeding the pet
def feed_pet():
    update_statistics()
    pet["Hunger"] = max(0, pet["Hunger"] - 15)
    pet["Health"] = min(100, pet["Health"] + 5)
    print(f"🍗 {pet['name']} has been fed. Hunger decreased and health improved") #lowers hunger and slightly improves health

# Playing with the pet
def play_with_pet():
    update_statistics()
    pet["Happiness"] += 10
    pet["Hunger"] += 5
    print(f"🎾 {pet['name']} had some fun, happiness increased:). But now he is hungry") #increases happiness but makes the pet more hungry

# Cleaning the pet
def clean_pet():
    update_statistics()
    pet["Health"] = min(100, pet["Health"] + 10) # improves the pets health by cleaning it
    print(f"🧼 {pet['name']} is all clean and refreshed!")

# Letting the pet sleep
def let_pet_sleep():
    update_statistics()
    pet["Health"] = min(100, pet["Health"] + 15)
    pet["Hunger"] += 5
    print(f"😴 {pet['name']} took a nice long nap.") # increases health but also slightly increases hunger

# Checking the pet's status
def check_status():
    update_statistics()
    if not pet["Alive"]:
        print(f"💀 You did not take care of {pet['name']}! {pet['name']} died! You need to start over:(")
        return

# display all the statistics of the pet
    print(f"\n🐾 {pet['name']}'s status:")
    print(f"🍗 Hunger: {pet['Hunger']}")
    print(f"😊 Happiness: {pet['Happiness']}")
    print(f"❤️ Health: {pet['Health']}\n")

# show warnings if the statistics of the pet are not good
    if pet["Hunger"] >= 80:
        print("⚠️ Your pet is very hungry! Feed them soon!")
    if pet["Happiness"] <= 20:
        print("😢 Your pet is sad! Play with them!")
    if pet["Health"] <= 30:
        print("⚠️ Your pet's health is low! Take care of them!")

# introduction to the game
def introduction():
    print("\n Welcome to your Virtual Pet Simulator! 🎉")
    print("In this game you will adopt a pet of your choice and you will have to take care of it as if it is your own child!")
    print("Take care of your pet by feeding, playing, cleaning and letting it rest ")
    print("But be careful! If you neglect your pet and don't look after it properly, it will die!!!!")
    print("So make sure you are a good parent and look after your pet properly")
    print("Save your progress and come back to check up on your pet regularly.")
    print("ENJOY😆")


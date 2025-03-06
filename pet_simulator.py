import json # save + load data about the pet
import time # helps when stats should decrease over time

#make a list of available pets to choose from
pet_types = ["Dog", "Cat", "Rabbit", "Hamster", "Fox", "Guinea Pig", "Panda"]

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
    """
    Saves the current pet data to a JSON file
    This function saves the pet's current state to 'pet_data.json' so that the progress can be saved and played later
    """
    with open("pet_data.json", "w") as f:
        json.dump(pet, f)
    print("✅ Game saved!")

# loading a saved (existing) game, if no save is found, it starts a new game
def load_game():
    """
    loads the previous pet data from a JSON file. In the case that the file is not found or the user wants to restart the game, it prompts the user to start a new game
    """
    global pet
    try:
        while True:
            choice = input("🔁 Do you want to continue playing with your previous pet? (yes/no) ")
            if choice == "yes":
                with open("pet_data.json", "r") as f:
                    pet = json.load(f)
                print(f"🎉 Welcome back! {pet['Name']} the {pet['Type']} is waiting for you")
                return # exit function after loading the game
            elif choice == "no":
                print("🚀 Starting a new game!")
                create_pet()
                return #exits the function after creating the new pet
            else:
                print("⚠️ Please enter 'yes' or 'no'.")
    except FileNotFoundError:
        print("⚠️ No saved game found. Let's create a new pet for you to take care of!")
        create_pet()

# Create a new pet and let the user choose its type (and making sure it is valid)
def create_pet():
    """
    Allows the user to create a new pet by choosing a name a pet type
    :return: none
    """
    pet["Name"] = input("🐾 Enter a name for your pet ").capitalize()

    while True:
        pet_type = input(f"Choose a pet type {pet_types}: ").capitalize()
        if pet_type in pet_types:
            pet["Type"] = pet_type
            break
        print("⚠️ Your choice is invalid, please choose a valid pet type")
    print(f"🎉 You adopted {pet['Name']} the {pet['Type']}! Make sure you take good care of them!")

# Updating the pets statistics over time
def update_statistics():
    """
    Updates the pets statistics based on how much time has passed
    :return: None
    """
    if not pet["Alive"]:
        return

    time_passed = time.time() - pet["Last_updated"]
    decay_amount = int(time_passed // 5) # every 10 seconds the statistics decay

    if decay_amount > 0:
        pet["Hunger"] = min(100, pet["Hunger"] + decay_amount)
        pet["Happiness"] = max(0, pet["Happiness"] - decay_amount)
        pet["Health"] = max(0, pet["Health"] - decay_amount // 2)
        pet["Last_updated"] = time.time()

        if pet["Hunger"] >= 100 or pet["Health"] <= 0: # if hunger reaches 100 or health reaches 0, the pet dies
            pet["Alive"] =False
            print(f"💀 {pet['Name']} has died... You did not take proper care of them.")

# Feeding the pet
def feed_pet():
    """
    Feeds the pet, decreasing hunger and slightly improves health
    :return: None
    """
    update_statistics()
    pet["Hunger"] = max(0, pet["Hunger"] - 15)
    pet["Health"] = min(100, pet["Health"] + 5)
    print(f"🍗 {pet['Name']} has been fed. Hunger decreased and health improved")

# Playing with the pet
def play_with_pet():
    """
    Plays with the pet, increases happiness but increases hunger
    :return: none
    """
    update_statistics()
    pet["Happiness"] += 10
    pet["Hunger"] += 5
    print(f"🎾 {pet['Name']} had some fun, happiness increased:). But now he is hungry")

# Cleaning the pet
def clean_pet():
    """
    Cleans the pet, improving it's health
    :return:
    """
    update_statistics()
    pet["Health"] = min(100, pet["Health"] + 10)
    print(f"🧼 {pet['Name']} is all clean and refreshed!")

# Letting the pet sleep
def let_pet_sleep():
    """
    Lets the pet sleep, increases health but also slightly increases hunger
    :return: None
    """
    update_statistics()
    pet["Health"] = min(100, pet["Health"] + 15)
    pet["Hunger"] += 5
    print(f"😴 {pet['Name']} took a nice long nap.")

# Checking the pet's status
def check_status():
    """
    Displays the current status of the pet, including hunger, happiness, and health.
    :return: None
    """
    update_statistics()

    if not pet["Alive"]:
        print(f"💀 You did not take care of {pet['Name']}! {pet['Name']} died! You need to start over:(")
        return

# display all the statistics of the pet
    print(f"\n🐾 {pet['Name']}'s status:")
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
    """
    Prints the introduction to the game. Displays a welcome message and explains the rules of the game.
    :return: None
    """
    print("\n Welcome to your Virtual Pet Simulator! 🎉")
    print("In this game you will adopt a pet of your choice and you will have to take care of it as if it is your own child!")
    print("Take care of your pet by feeding, playing, cleaning and letting it rest ")
    print("But be careful! If you neglect your pet and don't look after it properly, it will die!!!! 😢")
    print("So make sure you are a good parent and look after your pet properly 👨‍👩‍👧")
    print("Save your progress and come back to check up on your pet regularly.")
    print("ENJOY😆")

# Playing the game
def main_menu():
    """
    Runs the game loop, allowing the player to interact with their pet
    :return: None
    """
    introduction()
    load_game()

    while pet["Alive"]:
        check_status()

        print("\n1️⃣ Feed Pet")
        print("2️⃣ Play with Pet")
        print("3️⃣ Clean Pet")
        print("4️⃣ Let Pet Sleep")
        print("5️⃣ Do Nothing")
        print("6️⃣ Save & Exit")

        choice = input("Choose an action: ")

        if choice == "1":
            feed_pet()
        elif choice == "2":
            play_with_pet()
        elif choice == "3":
            clean_pet()
        elif choice == "4":
            let_pet_sleep()
        elif choice == "5":
            update_statistics()
            print("⏳ Time passes... Your pet is waiting.")
        elif choice == "6":
            save_game()
            print("👋 Game saved! See you next time!")
            break
        else:
            print("⚠️ Invalid choice, try again!")

if __name__ == "__main__":
    main_menu()



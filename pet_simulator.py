import json # save + load data about the pet
import time # helps when stats should decrease over time
import random # adds randomness for events & mini games

#make a list of available pets to choose from
pet_types = ["Dog", "Cat", "Rabbit", "Hamster", "Fox", "Guinea Pig", "Panda"]

# make the default statistics for the pet
pet = {
    "Name": "", #chosen by the user
    "Type": "", #chosen by the user
    "Hunger": 50, #starts at 50 (higher is worse)
    "Happiness": 50, #starts at 50 (higher is better)
    "Health": 50, #starts at 50 (higher is better but drops over time)
    "Coins": 10, # currency system for the shop
    "Last_updated": time.time(), #tracks the time for the statistics to decrease
    "Alive": True #if False, the pet has died
}

# Shop items
shop_items = {
    "Food": {"cost": 5, "Hunger": -15},
    "Toy": {"cost": 10, "Happiness": +20},
    "Medicine": {"cost": 15, "Health": +15}
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

# random events feature
def random_event():
    """
    Triggers a random event occasionally
    Events can increase/decrease pets status and give rewards
    :return: none
    """
    events = [
        ("🍖 Your pet found a hidden treat! ", "Health", 5, "Hunger", -5),
        ("😢 Your pet is feeling lonely. Happiness -10", "Happiness", -10),
        ("🎩 Your pet learned a trick! +10 Happiness", "Happiness", 10),
        ("💰 You found some coins! +5 Coins", "Coins", 5),
    ]

    if random.randint(1, 3) == 1:  # 33% chance of event occurring
        event, stat1, change1, *rest = random.choice(events) # random.choice(events) picks a random tuple from the events list
        pet[stat1] = min(100, max(0, pet[stat1] + change1)) # accesses the pet's stat dictionary, applies the change, prevents the stat from going below 0 and above 100

        if rest: # checks if there is a second stat in the event, and if there is it does the same thing as previously
            stat2, change2 = rest
            pet[stat2] = min(100, max(0, pet[stat2] + change2))

        print(event)

#Playing rock, paper, scissors
def play_rps():
    """
    Play Rock-Paper-Scissors with your pet.
    Winning gives you +2 Coins. Losing or drawing does nothing.
    """
    moves = ["rock", "paper", "scissors"]

    print("\n🎮 Let's play Rock-Paper-Scissors!")
    print("🪨 Rock  📄 Paper  ✂️ Scissors")

    player_choice = input("Choose (rock, paper, scissors): ").strip().lower()

    if player_choice not in moves:
        print("⚠️ Invalid choice! Please pick rock, paper, or scissors.")
        return

    pet_choice = random.choice(moves)

    print(f"🐾 {pet['Name']} chose {pet_choice}!")

    if player_choice == pet_choice:
        print("😮 It's a draw! No coins earned.")
    elif (player_choice == "rock" and pet_choice == "scissors") or \
            (player_choice == "paper" and pet_choice == "rock") or \
            (player_choice == "scissors" and pet_choice == "paper"):
        print("🎉 You win! You earned +2 Coins!")
        pet["Coins"] += 2  # ✅ Add 2 coins for winning
    else:
        print("😢 You lost! No coins earned.")


# Updating the pets statistics over time
def update_statistics():
    """
    Updates the pets statistics based on how much time has passed
    :return: None
    """
    if not pet["Alive"]:
        return

    time_passed = time.time() - pet["Last_updated"]
    decay_amount = int(time_passed // 5) # every 5 seconds the statistics decay

    if decay_amount > 0:
        pet["Hunger"] = min(100, pet["Hunger"] + decay_amount)
        pet["Happiness"] = max(0, pet["Happiness"] - decay_amount)
        pet["Health"] = max(0, pet["Health"] - decay_amount // 2)
        pet["Last_updated"] = time.time()

        if pet["Hunger"] >= 100 or pet["Health"] <= 0: # if hunger reaches 100 or health reaches 0, the pet dies
            pet["Alive"] =False
            print(f"💀 {pet['Name']} has died... You did not take proper care of them.")

    random_event()

# Get pet mood
def get_mood():
    """ Returns the pet's mood based on happiness level. """
    if pet["Happiness"] >= 80:
        return "🥰 Very Happy"
    elif pet["Happiness"] >= 50:
        return "🙂 Content"
    elif pet["Happiness"] >= 30:
        return "😕 Unhappy"
    else:
        return "😡 Angry"

# Shop system
def shop():
    """ Allows the user to buy food, toys, or medicine for their pet. """
    while True:
        print("\n🛒 Welcome to the Pet Shop!")
        print(f"💰 You have {pet['Coins']} coins.")

        print("Here are all the available items: ")
        for i, (item, details) in enumerate(shop_items.items(), start=1):
        # loops through the dictionary of shop_items
        # assigns item numbers from 1 for easy selection
            print(f"{i}️ {item.capitalize()} - {details['cost']} Coins")

        print("0️⃣ Exit shop")

        choice = input("Choose an item to buy: ").strip() # gets the player's choice and removes accidental spaces

        if choice == "0":
            print("👋 Leaving shop, see you next time!")
            break

        items_list = list(shop_items.keys()) # converts the dictionary keys into a list

        if choice in ["1", "2", "3"]:
            item = items_list[int(choice) - 1] # converts the choice string to an index number
            if pet["Coins"] >= shop_items[item]["cost"]: # checks if the player has enough coins
                pet["Coins"] -= shop_items[item]["cost"] # reduces the amount of coins by the item's cost
                for stat, value in shop_items[item].items(): # loops through the items effects
                    if stat != "cost": # excludes cost because it is not a statistic of the pet
                        pet[stat] = min(100, max(0, pet[stat] + value)) # stats can't go below 0 or above 100
                print(f"✅ You bought {item.capitalize()}!")
            else:
                print("❌ Not enough coins!")
        else:
            print("⚠️ Invalid choice! Returning to the menu")

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
    print("\nIn this game you will adopt a pet of your choice and you will have to take care of it as if it is your own child!")
    print("Take care of your pet by feeding, playing, cleaning and letting it rest ")
    print("\nBut be careful! If you neglect your pet and don't look after it properly, it will die!!!! 😢")

    print("\n🛒 The Shop")
    print("Earn coins and visit the shop to buy food, toys, and medicine for your pet.")
    print("Each item helps maintain your pet's well-being.")

    print("\n🎮 Play Rock-Paper-Scissors")
    print("Challenge your pet in a fun game of Rock-Paper-Scissors!")
    print("Win the game to earn extra coins, which you can use in the shop.")

    print("\n🎲 Random Events")
    print("Unexpected things can happen to your pet! Sometimes good, sometimes bad.")
    print("Keep checking on your pet to see what surprises await!")

    print("\nSo make sure you are a good parent and look after your pet properly 👨‍👩‍👧")
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
        print("6️⃣ Visit the shop")
        print("7️⃣ Play Rock-Paper-Scissors")
        print("8️⃣ Save & Exit")

        try:
            choice = input("Choose an action: ").strip()
        except KeyboardInterrupt:
            print("\n⛔ Game interrupted! Exiting safely...")
            save_game()
            print("👋 Goodbye!")
            break  # Exit safely

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
            shop()
        elif choice == "7":
            play_rps()
        elif choice == "8":
            save_game()
            print("👋 Game saved! See you next time!")
            break
        else:
            print("⚠️ Invalid choice, try again!")

if __name__ == "__main__":
    main_menu()



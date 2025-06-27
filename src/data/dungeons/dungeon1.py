def run_dungeon(menu):
    menu.add_text("Dungeon 1: Jumping Goblin Cave")
    menu.add_text("You enter a dark cave filled with nothing but darkness.")
    menu.add_text("You hear a faint sound of water dripping but besides that, it's silent.")
    menu.add_text("You see a faint light in the distance, you walk towards it.")
    menu.add_text("Event: You find a torch.")
    menu.add_text("You light the torch and the cave is illuminated.")
    menu.add_text("You see two paths leading deeper into the cave.")

    first_choice = menu.choose(["Go left", "Go right"])

    if first_choice == 0:
        menu.add_text("You find a dead end with a few bones scattered around.")
        menu.add_text("Do you want to go back or look around?")
        sub_choice = menu.choose(["Go back", "Look around"])
        if sub_choice == 1:
            menu.add_text("You find even more bones and a rusty sword.")
            menu.add_text("There is nothing useful here, you decide to go back.")
        else:
            menu.add_text("You go back to the main path.")

    if first_choice == 1:
        menu.add_text("You find once again two paths leading deeper into the cave.")
        menu.add_text("Do you want to go left or straight?")
        sub_choice = menu.choose(["Go left", "Go straight"])
        if sub_choice == 0:
            menu.add_text("You find a goblin! It didn't see you, do you want to attack it or go back?")
            goblin_choice = menu.choose(["Attack it", "Go back"])
            if goblin_choice == 0:
                menu.fight("Goblin", 50)
                menu.add_text("You defeated the goblin.")
            else:
                menu.add_text("You quietly go back to the previous fork.")
        else:
            menu.add_text("You walk straight ahead, but the path is empty and eerily quiet.")

    menu.fight("Goblin", 50)
    menu.fight("Goblin Warrior", 70)
    menu.add_text("You survived the jumping goblin cave!")
def run_dungeon(display_surface):
    # Customize events, enemies, etc. here
    import pygame
    from setup_settings.dungeon_menu import DungeonMenu

    menu = DungeonMenu(display_surface, None)  # Use None or a custom function if needed
    menu.add_text("Dungeon 1: jumping goblin cave")
    menu.add_text("You enter a dark cave filled with nothing but darkness.")
    menu.add_text("You hear a faint sound of water dripping but besides that, it's silent.")
    menu.add_text("You see a faint light in the distance, you walk towards it.")
    menu.add_text("Event: You find a torch.")
    menu.add_text("You light the torch and the cave is illuminated.")
    menu.add_text("You see two paths leading deeper into the cave.")
    first_choice(menu)

    menu.fight("Goblin", 50)
    menu.fight("Goblin Warrior", 70)
    return menu.player_health  # Return updated HP

def first_choice(menu):
    import pygame
    from setup_settings.dungeon_menu import DungeonMenu

    menu = DungeonMenu(pygame.display.get_surface(), None)  # Use None or a custom function if needed
    menu.add_text("You can either go left or right.")
    
    choice = menu.choice(["Left", "Right"])
    
    if choice == "Left":
        menu.add_text("You find a dead end with a few bones scattered around.")
        menu.add_text("Do you want to go back or look around?")
        sub_choice = menu.choice(["Go Back", "Look Around"])
    
        if sub_choice == "Look Around":
            menu.add_text("You find even more bones and a rusty sword.")
            menu.add_text("There is nothing useful here, you decide to go back.")
    
        if sub_choice == "Go Back":
            menu.add_text("You go back to the main path.")


    if choice == "Right":  
        menu.add_text("You find once again two paths leading deeper into the cave.")
        menu.add_text("Do you want to go left or straight?")
        sub_choice = menu.choice(["go left", "straight"])
    
        if sub_choice == "go left":
            menu.add_text("You find a goblin!")
            menu.add_text("It didn't see you, do you want to attack it or go back?")

        if sub_choice == "attack it":
            menu.fight("Goblin", 50)
            menu.add_text("You defeated the goblin.")
            
    

        if sub_choice == "straight":
            menu.add_text(".")

    return choice    
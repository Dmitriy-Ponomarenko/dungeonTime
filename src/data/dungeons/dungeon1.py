def run_dungeon(menu):
    menu.add_text("Dungeon 1: Tunnels of the shadow mountain")
    menu.add_text("You enter an empty looking cave.")
    menu.add_text("You hear nothing but the wind howling through the empty tunnels.")
    choice = menu.choose(["Leave the cave", "Continue the journey"])
    if choice == 0:
        menu.add_text("You look back one more time, seeing the darkness of the cave behind you. You decide to leave the cave.")
        return
    elif choice == 1:
        menu.add_text("You make your way deeper into the darkness. Your eyes couldn't pick up everything, but you see something on the wall.")
        menu.add_text("Event: You find a torch!")
        menu.player_inventory.append("torch")
        menu.add_text("Now having light, you make your way deeper into the cave.")
        menu.add_text("You soon heard a noise very close to you. Oh no! A goblin! What will you do?")
        fight_choice = menu.choose([
            "Attack quickly",
            "Attack with a strong blow",
            "Dodge and counter",
            "Try to talk to it"
        ])
        if fight_choice == 0:
            menu.add_text("You attack the goblin quickly and manage to hit it!")
            menu.fight("Goblin", 50)
        elif fight_choice == 1:
            menu.add_text("You prepare a strong blow and manage to land a critical hit!")
            menu.fight("Goblin", 70)
        elif fight_choice == 2:
            menu.add_text("You dodge the goblin's attack and counter!")
            menu.fight("Goblin", 60)
        elif fight_choice == 3:
            menu.add_text("You try to talk to the goblin.")
            menu.add_text("The goblin is not interested in talking and attacks!")
            menu.fight("Goblin", 50)

    menu.add_text("You catch your breath, thankfully you were still alive. Now you continued to walk deeper into the cave.")
    menu.add_text("Till now there is nothing. Athough you feel like you are being watched.")
    menu.add_text("Suddenly, a group of goblins appear from the shadows!")
    fight_choice = menu.choose([
        "Fight the goblins",
        "Try to sneak past them",
        "Use a distraction"
    ])
    if fight_choice == 0:
        menu.fight("Goblin", 50)
    elif fight_choice == 1:
        menu.add_text("You attempt to sneak past the goblins.")
        menu.add_text("Luckily they don't notice you and you slip by!")
    elif fight_choice == 2:
        menu.add_text("You throw a rock to create a distraction.")
        menu.add_text("The goblins investigate the noise.")
        menu.add_text("You manage to slip past them!")

    menu.add_text("You reach a large chamber with a strange altar in the center.")
    menu.add_text("The air feels charged with magic.")
    menu.add_text("You see a glowing crystal on the altar.")
    menu.add_text("Oh no! A goblin shaman appears! That is what was watching you! The prophecy was true!")
    menu.add_text("It looks like it is ready to fight!")
    boos_choice = menu.choose([
        "Charge with all your might",
        "find a way to escape",
        "try to distract the goblin shaman",
        "Taunt the goblin shaman"
    ])
    if boos_choice == 0:
        menu.add_text("You charge at the goblin shaman with all your might!")
        menu.fight("Goblin Shaman", 100)
    elif boos_choice == 1:
        menu.add_text("You try to find a way to escape.")
        menu.add_text("The goblin shaman is too powerful, you need to fight!")
        menu.fight("Goblin Shaman", 100)
    elif boos_choice == 2:
        menu.add_text("You try to distract the goblin shaman with a rock.")
        menu.add_text("The goblin shaman is momentarily distracted.")
        menu.fight("Goblin Shaman", 100)
        menu.add_text("You take advantage of the distraction and attack!")
        menu.fight("Goblin Shaman", 100)
    elif boos_choice == 3:
        menu.add_text("You try to taunt the goblin shaman.")
        menu.add_text("The goblin shaman is enraged and attacks!")
        menu.fight("Goblin Shaman", 100)

    menu.add_text("You have survived the Tunnels of the Shadow Mountain!")
     
       

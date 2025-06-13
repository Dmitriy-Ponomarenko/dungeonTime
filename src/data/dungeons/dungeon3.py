def run_dungeon(menu):
    menu.add_text("Dungeon 3: Tomb of the Draugr")
    menu.add_text("You enter a cold, dark tomb. The air is thick with the scent of decay.")
    menu.add_text("Your footsteps echo. You feel a chill run down your spine.")
    menu.add_text("You see the remains of a fallen adventurer. Do you search the body?")
    choice = menu.choose(["Yes, search the body", "No, move on"])
    if choice == 0:
        menu.add_text("You kneel beside the body, feeling uneasy.")
        menu.add_text("You find a healing potion and a rusty sword.")
        menu.player_inventory.append("healing potion")
        menu.add_text("You wonder what fate befell this poor soul...")
    else:
        menu.add_text("You decide not to disturb the dead and move deeper into the tomb.")

    menu.add_text("A faint whisper echoes: 'Turn back...'")
    menu.add_text("Suddenly, a draugr emerges from the shadows, sword raised!")
    fight_choice = menu.choose([
        "Attack quickly",
        "Attack with a strong blow",
        "Dodge and counter",
        "Try to talk to it"
    ])
    if fight_choice == 0:
        menu.add_text("You lunge forward, hoping speed will win the day.")
        menu.fight("Draugr", 40, player_action="quick")
    elif fight_choice == 1:
        menu.add_text("You gather your strength for a powerful blow.")
        menu.fight("Draugr", 60, player_action="strong")
    elif fight_choice == 2:
        menu.add_text("You try to dodge its attack and counter.")
        menu.fight("Draugr", 40, player_action="dodge")
    else:
        menu.add_text("You try to speak: 'I mean you no harm!'")
        menu.add_text("The draugr hesitates, but then attacks anyway!")
        menu.fight("Draugr", 40, player_action="quick")

    menu.add_text("You catch your breath and press on.")
    menu.add_text("Deeper in, you find two paths: one lit by eerie blue flames, the other shrouded in darkness.")
    path_choice = menu.choose(["Take the blue flame path", "Venture into the darkness"])
    if path_choice == 0:
        menu.add_text("You follow the blue flames. The air feels charged with magic.")
        menu.add_text("You find a magical rune that boosts your strength!")
        menu.player_stats["strength"] += 2
        menu.add_text("You feel a surge of power course through your veins.")
    else:
        menu.add_text("You step into the darkness, feeling your way along the wall.")
        menu.add_text("You stumble upon a group of draugr feasting on another adventurer.")
        menu.add_text("You try to sneak past, but one notices you!")
        menu.fight("Draugr Pack", 80, player_action="group")

    menu.add_text("You reach the burial chamber. The Draugr Lord awakens!")
    boss_choice = menu.choose([
        "Charge with all your might",
        "Try to sneak and backstab",
        "Use a healing potion",
        "Taunt the Draugr Lord"
    ])
    if boss_choice == 2 and "healing potion" in menu.player_inventory:
        menu.add_text("You quickly drink your healing potion.")
        menu.player_health += 30
        menu.player_inventory.remove("healing potion")
        menu.add_text("You feel your wounds close and your strength return.")
    elif boss_choice == 2:
        menu.add_text("You reach for a potion, but your bag is empty!")
    menu.fight("Draugr Lord", 120, player_action="boss")

    menu.add_text("You have survived the Tomb of the Draugr!")

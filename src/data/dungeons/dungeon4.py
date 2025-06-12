def run_dungeon(display_surface):
    # Customize events, enemies, etc. here
    import pygame
    from setup_settings.dungeon_menu import DungeonMenu

    menu = DungeonMenu(display_surface, None)  # Use None or a custom function if needed
    menu.add_text("Dungeon 1: Dark Caverns")
    menu.fight("Skeleton", 50)
    menu.add_text("Event: You find a torch.")
    menu.fight("Skeleton Warrior", 70)
    return menu.player_health  # Return updated HP

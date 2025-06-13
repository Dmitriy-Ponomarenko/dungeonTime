def run_dungeon(display_surface):
    import pygame
    from setup_settings.dungeon_menu import DungeonMenu

    menu = DungeonMenu(display_surface, None)

    # Story-Variablen
    selene_begleiterin = False
    selene_verraet_dich = False

    # DUNGEON START
    menu.add_text("🧙‍♀️ Ebene 3: Prüfung der Elemente")
    menu.add_text("Du triffst auf Selene, die Magierin. Sie steht vor einem magischen Schrein.")
    menu.add_text("Sie mustert dich misstrauisch.")

    # Entscheidung über Selene
    entscheidung = menu.choose([
        "1) Mit ihr reden & Prüfung ablegen",
        "2) Schrein zerstören",
        "3) Sie anlügen und später verraten"
    ])

    if entscheidung == 0:
        selene_begleiterin = True
        menu.add_text("Selene: 'Beweise deine Ehre.'")
        menu.fight("Elementargeist", 60)
        menu.add_text("🎉 Du bestehst die Prüfung. Selene schließt sich dir an.")
    elif entscheidung == 1:
        menu.add_text("Du zerstörst den Schrein.")
        menu.add_text("Selene: 'Du Narr!'")
        menu.fight("Selene, die Magierin", 100)
        return menu.player_health
    elif entscheidung == 2:
        selene_begleiterin = True
        selene_verraet_dich = True
        menu.add_text("Du tust so, als wärst du auf ihrer Seite...")
        menu.add_text("Selene: 'Dann kämpfen wir zusammen.'")

    # Chronosstein-Szene
    menu.add_text("🔮 Du findest später den CHRONOSSTEIN – Quelle mächtiger Zeitmagie.")
    chrono = menu.choose([
        "1) Den Chronosstein nutzen",
        "2) Den Chronosstein zerstören"
    ])

    if chrono == 0:
        menu.add_text("Du nutzt die Macht des Chronossteins...")
        if selene_begleiterin and not selene_verraet_dich:
            menu.add_text("Selene: 'Ich h_"
)
 
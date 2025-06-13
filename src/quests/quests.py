class Quest:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        # torik_event.py

print("🏰 Du gehst in die Katakomben der Toten...")
print("🧍 Dort kämpft ein Krieger gegen Schatten – sein Name ist Torik.")

print("\nWas willst du tun?")
print("1 - Torik helfen")
print("2 - Torik ignorieren")
print("3 - Torik angreifen (nur mit Schattenpakt)")

entscheidung = input("Deine Wahl (1/2/3): ")

if entscheidung == "1":
    print("\n✅ Du hilfst Torik. Er wird dein Begleiter!")
elif entscheidung == "2":
    print("\n☠️ Du ignorierst Torik. Er stirbt... und du bekommst mehr Feinde.")
elif entscheidung == "3":
    print("\n⚔️ Du greifst Torik an. Er wird später ein Mini-Boss!")
else:
    print("\n❌ Ungültige Eingabe.")

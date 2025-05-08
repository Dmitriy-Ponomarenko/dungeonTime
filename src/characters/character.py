class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def attack(self, target):
        # Placeholder for attack logic
        pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def attack(self, target):
        pass  # Implement attack logic here

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0


class Enemy(Character):
    def __init__(self, name, health, attack_power):
        super().__init__(name, health)
        self.attack_power = attack_power

    def attack(self, target):
        target.take_damage(self.attack_power)  # Enemy attacks target with attack_power

    def __str__(self):
        return f"{self.name} (Enemy) - Health: {self.health}, Attack Power: {self.attack_power}"
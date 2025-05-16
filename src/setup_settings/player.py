from .settings import * 

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.image = pygame.Surface((48,56))
		self.image.fill('red')
		self.rect = self.image.get_rect(topleft = pos)

		# movement 
		self.direction = vector()
		self.speed = 200

	def input(self):
		keys = pygame.key.get_pressed()
		input_vector = vector(0, 0)
		# Arrow keys
		if keys[pygame.K_RIGHT]:
			input_vector.x += 1
		if keys[pygame.K_LEFT]:
			input_vector.x -= 1
		if keys[pygame.K_DOWN]:
			input_vector.y += 1
		if keys[pygame.K_UP]:
			input_vector.y -= 1
		# WASD keys
		if keys[pygame.K_d]:
			input_vector.x += 1
		if keys[pygame.K_a]:
			input_vector.x -= 1
		if keys[pygame.K_s]:
			input_vector.y += 1
		if keys[pygame.K_w]:
			input_vector.y -= 1

		if input_vector.length() > 0:
			self.direction = input_vector.normalize()
		else:
			self.direction = vector(0, 0)

	def move(self, dt):
		self.rect.topleft += self.direction * self.speed * dt

	def update(self, dt):
		self.input()
		self.move(dt)





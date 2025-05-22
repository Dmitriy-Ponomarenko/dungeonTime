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
		# jump
		self.is_jumping = False
		self.jump_count = 10
	
	def jump(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			if not self.is_jumping:
				self.is_jumping = True

		if self.is_jumping:
			if self.jump_count >= -10:
				neg = 1
				if self.jump_count < 0:
					neg = -1
				self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
				self.jump_count -= 1
			else: 
				self.is_jumping = False
				self.jump_count = 10	

	def attack(self):
		keys = pygame.key.get_pressed()
		if pygame.mouse.get_pressed()[0]:
			self.is_attacking = True
		else:
			self.is_attacking = False

	def special_skill(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_e]:
			self.is_special_skill = True
		else:
			self.is_special_skill = False	

	def shield(self):
		# Implement the shield logic here
		pass 
    
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
		# Jump
		if keys[pygame.K_SPACE]:
			self.jump()
		# Attack
		if keys[pygame.K_LCTRL]:
			self.attack()
		# Special skill
		if keys[pygame.K_e]:
			self.special_skill()
		# shield
		if keys[pygame.K_q]:
			self.shield()


		if input_vector.length() > 0:
			self.direction = input_vector.normalize()
		else:
			self.direction = vector(0, 0)

	def move(self, dt):
		self.rect.topleft += self.direction * self.speed * dt

	def update(self, dt):
		self.input()
		self.move(dt)
		self.jump()
		self.attack()
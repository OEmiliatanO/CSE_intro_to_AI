from random import randint
import pygame

class Bird(pg.sprite.Sprite):
	def __init__(self, canv, scope = 50):
		super().__init__()
		self.canv = canv
		self.image = pygame.Surface((15, 15))
		Color = pg.Color(randint(0,255), randint(0,255), randint(0,255))
		pygame.draw.polygon(self.image, Color, ((0,0),(0,3),(1.5,1.5),(3,1.5)))
		Width, Height = self.canv.get_size()
		self.angle = randint(0, 360)
		self.v = pygame.Vector2(math.cos(self.angle * math.pi / 180), math.sin(self.angle * math.pi / 180))
		self.rect = self.image.get_rect(center = (randint(20, Width - 20), randint(20, Height - 20)))
		self.pos = pygame.Vector2(self.rect.cent)
		self.scope = scope
	def update(self, birdslist, dt):
		Width, Height = self.canv.get_size()


def main():
	pygame.init()
	width, height = 900, 900
	pygame.display.set_caption("boids")
	screen = pygame.display.set_mode((width, height), pygame.RESIZEABLE)
	dt = 0.0001

	birdgp = pygame.sprite.Group()
	for i in range(n):
		birdgp.add(Bird(screen))
	birdslist = birdgp.sprites()
	while True:
		screen.fill((0, 0, 0))
		birdgp.update(birdslist, dt)
		birdgp.draw(screen)
		birdgp.display.update()

if __name__ == '__main__':
	main()
	pygame.quit()

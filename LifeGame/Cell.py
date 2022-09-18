
class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.isalive = False
		self.nexAlive = False
		self.drawed = False

	def draw(self, canv, scale = 10):
		color = 'white'
		if not self.isalive:
			self.drawed = False
			color = 'black'
		rx = self.x * scale + scale
		by = self.y * scale + scale
		canv.create_rectangle(self.x * scale, self.y * scale, rx, by, fill = color)
		self.drawed = True

	def detect(self, n):
		match n:
			case 0|1:
				self.nexAlive = False
				return
			case 2|3:
				if not self.isalive and n == 3:
					self.nexAlive = True
				return
			case 4|5|6|7|8:
				self.nexAlive = False
				return

	def transform(self, canv):
		if self.isalive == self.nexAlive and self.drawed:
			return
		self.isalive = self.nexAlive
		self.draw(canv)

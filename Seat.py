class Seat:
	row = None
	column = None
	position = (0, 0)
	is_sold = False
	is_barrier = False
	is_properly_distanced = True

	def __init__(self, row, col):
		self.row = row
		self.column = col
		self.position = self.alphabetic_row() + str(col)

	def __str__(self):
		return "s" if not self.is_sold or self.is_barrier else "#"

	def alphabetic_row(self):
		return chr(self.row + 64)

	def set_sold(self):
		self.is_sold = True

	def set_barrier(self):
		self.is_barrier = True


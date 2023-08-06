class human:
	gender=None
	def set_gender(self, value):
		self.gender = value
		return ''

sufian = human()
sufian.set_gender(input("Enter your Gender: "))
print("The gender is set to: " + sufian.gender)

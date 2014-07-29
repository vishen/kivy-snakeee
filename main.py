import kivy
kivy.require('1.8.0')

import random

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

SPEED = 0.1

class Snake(Widget):

	unusable_directions = {
		"right": "left",
		"left": "right",
		"up": "down",
		"down": "up",
	}

	direction = "down"
	body = []
	body_size = 30.
	food = None

	points = NumericProperty(0)
	score = None

	def __init__(self, *args, **kwargs):
		super(Snake, self).__init__(*args, **kwargs)

		self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text") 
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

		self._initialize_game()

	def _initialize_game(self):
		self.body = []
		self.score = None
		self.food = None
		self.points = 0
		self.direction = "down"

		self.canvas.clear()
		size = self.body_size
		with self.canvas:
			Color(0, 0, 1)
			head = Rectangle(pos=[300, 300], size=(size, size))
			self.body.append(head)


			x, y = self.generate_food_position()

			Color(0, 1, 0)
			self.food = Rectangle(pos=[x, y], size=(size, size))

		self.score = Label(font_size=70, text=str(self.points))
		self.add_widget(self.score)


	def generate_food_position(self):

		size = self.body_size
		window_size = Window.size

		while True:
			x = random.randint(size, window_size[0] - size)
			y = random.randint(size, window_size[1] - size)

			x -= (x % size)
			y -= (y % size)

			found = False
			for b in self.body:
				if b.pos == [x, y]:
					found = True

			if not found:
				return x, y

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self.on_key_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifier):
		_direction = keycode[1]
		if self.unusable_directions[_direction] != self.direction:
			self.direction = _direction

	def _update_body(self, front_pos, add_new=False):
		next_pos = front_pos
		for i in range(len(self.body)):
			tmp = self.body[i].pos
			self.body[i].pos = next_pos
			next_pos = tmp

		if add_new:
			with self.canvas:
				Color(0, 0, 1)
				bp = Rectangle(pos=next_pos, size=(self.body_size, self.body_size))
				self.body.append(bp)

	def update(self, dt):
		
		size = self.body_size

		new_pos = list(self.body[0].pos)

		if self.direction == "right":
			new_pos[0] += size
		elif self.direction == "left":
			new_pos[0] -= size
		elif self.direction == "up":
			new_pos[1] += size
		elif self.direction == "down":
			new_pos[1] -= size

		game_over = False
		window_size = Window.size
		if new_pos[0] < 0 or new_pos[1] < 0:
			game_over = True

		elif new_pos[0] + size > window_size[0] or\
			  new_pos[1] + size > window_size[1]:
			  game_over = True

		for b in self.body[1:]:
			if list(b.pos) == new_pos:
				game_over = True


		if game_over:
			Clock.unschedule(self.update)
			self.canvas.clear()
			l = Label(font_size=20, pos=(300, 300), 
					text="Game Over! Score: %d points" % self.points)

			def _play_again(*args, **kwargs):
				self._initialize_game()
				Clock.schedule_interval(self.update, SPEED)

			b = Button(text="Play Again?")
			b.on_release = _play_again
			self.add_widget(l)
			self.add_widget(b)

			return

		food_pos = self.food.pos
		ate_food = False
		if food_pos[0]  in (new_pos[0], new_pos[0] + size) and \
			food_pos[1] in (new_pos[1], new_pos[1] + size):

			self.points += 1
			self.score.text = str(self.points)

			x, y = self.generate_food_position()

			self.food.pos = [x, y]

			ate_food = True



		self._update_body(new_pos, ate_food)

			

			


		


class GameApp(App):

	def build(self):
		self.snake = Snake()
		Clock.schedule_interval(self.snake.update, SPEED)
		return self.snake


if __name__ == '__main__':
    app = GameApp()
    app.run()

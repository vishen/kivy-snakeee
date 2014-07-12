import kivy
kivy.require('1.8.0')

import random

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget

SPEED = 0.3

class Snake(Widget):

	unusable_directions = {
		"right": "left",
		"left": "right",
		"up": "down",
		"down": "up",
	}

	food_pos = None

	direction = "down"
	body = [[300, 300], [330, 300], [360, 300]]
	body_size = 30.

	def __init__(self, *args, **kwargs):
		super(Snake, self).__init__(*args, **kwargs)

		self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text") 
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		# self.update()

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self.on_key_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifier):
		_direction = keycode[1]
		if self.unusable_directions[_direction] != self.direction:
			self.direction = _direction
			# self.update()

	def _update_body(self, front_pos):
		next_pos = front_pos
		for i in range(len(self.body)):
			tmp = self.body[i]
			self.body[i] = next_pos
			next_pos = tmp

	def update(self, dt):
		
		size = self.body_size

		new_pos = list(self.body[0])

		if self.direction == "right":
			new_pos[0] += size
		elif self.direction == "left":
			new_pos[0] -= size
		elif self.direction == "up":
			new_pos[1] += size
		elif self.direction == "down":
			new_pos[1] -= size

		self._update_body(new_pos)

		self.canvas.clear()
		with self.canvas:
			# Draw food.
			if not self.food_pos:
				x = random.randint(1, self.size[1])
				y = random.randint(1, self.size[0])
				
				self.food_pos = [x, y]
			Color(0, 1, 0)
			Rectangle(pos=self.food_pos, size=(size, size))

			# Draw body first.
			Color(1, 0, 0)
			if len(self.body) > 1:
				for b in self.body[1:]:
					Rectangle(pos=b, size=(size, size))

			# Draw head last
			Color(0, 0, 1)
			Rectangle(pos=self.body[0], size=(size, size))


class GameApp(App):

	def build(self):
		self.snake = Snake()
		Clock.schedule_interval(self.snake.update, SPEED)
		return self.snake


if __name__ == '__main__':
    app = GameApp()
    app.run()

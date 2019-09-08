from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App

from functools import partial
import os

Builder.load_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'GoalMoveArea.kv'))

class GoalMoveArea(Widget):
	# Denotes if goal area has been touched and the element is currently floating
	touched = BooleanProperty(False)

	# The GoalObject that contains this instance of GoalMoveArea
	goal_object = ObjectProperty(None)

	# Scroll the sreen in case we come close to an edge
	def scroll_if_necessary(self, touch, scroll_view, *args):
		if not self.touched:
			return
		new_pos = scroll_view.scroll_y
		scrolling_pixels_amount = min(abs(touch.y - scroll_view.y), abs(touch.y - scroll_view.y))//10
		# print(scroll_view.y, touch.y)
		if touch.y - scroll_view.y < 50 and scroll_view.scroll_y != 0:
			# print(new_pos, new_pos + scroll_view.convert_distance_to_scroll(0, 1)[1])
			new_pos -= scroll_view.convert_distance_to_scroll(0, 1)[1]
			self.scrolled_amount += 1
		# print(touch.y, scroll_view.y, scroll_view.height)
		if (scroll_view.y + scroll_view.height) - touch.y < 50 and scroll_view.scroll_y != 1:
			new_pos += scroll_view.convert_distance_to_scroll(0, 1)[1]
			self.scrolled_amount -= 1
		
		scroll_view.scroll_y = min(1, max(0, new_pos))
		Clock.schedule_once(partial(self.scroll_if_necessary, touch, scroll_view))

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			# Make element transparent
			touch.grab(self)
			self.touched = True
			self.scrolled_amount = 0
			self.last_touch = touch.y

			# Create a scatter to hold floating element
			goal_object_copy = self.goal_object.copy()
			
			scroll_view = self.goal_object.parent.parent
			Clock.schedule_once(partial(self.scroll_if_necessary, touch, scroll_view))

			# Set correct absolute position and size
			goal_object_copy.pos = self.goal_object.to_window(self.goal_object.x, self.goal_object.y)
			goal_object_copy.size = self.goal_object.size

			# Place object absolutely
			goal_object_copy.size_hint = (None, None)
			self.floating_goal_object = goal_object_copy
			App.get_running_app().root.get_screen("main").add_widget(goal_object_copy)
			return True

	def on_touch_move(self, touch):
		if touch.grab_current is self:
			# Adjust position of the floating element
			self.floating_goal_object.y += touch.y-self.last_touch + self.scrolled_amount
			self.scrolled_amount = 0
			self.last_touch = touch.y

			# Check if we need to swap elements and swap them if necessary
			parent = self.goal_object.parent
			children = parent.children[:]

			# find position of floating element in its parent
			cur = 0
			for i in range(len(children)):
				if children[i] == self.goal_object:
					cur = i
					break

			# Check if we need swapping with element above
			while cur != len(children)-1 and children[cur+1].to_window(0, children[cur+1].y)[1] < touch.y:
				# Swap cur and cur+1
				parent.remove_widget(children[cur])
				parent.remove_widget(children[cur+1])
				parent.add_widget(children[cur], cur)
				parent.add_widget(children[cur+1], cur)
				cur += 1

			# Check if we need swapping with element below
			while cur != 0 and children[cur-1].height + children[cur-1].to_window(0, children[cur-1].y)[1] > touch.y:
				# Swap cur and cur-1
				parent.remove_widget(children[cur])
				parent.remove_widget(children[cur-1])
				parent.add_widget(children[cur-1], cur-1)
				parent.add_widget(children[cur], cur-1)
				cur -= 1
			# Scroll up/down if necessary


	def on_touch_up(self, touch):
		if touch.grab_current is self:
			# Make element no longer transparent
			touch.ungrab(self)
			self.touched = False

			# Remove widget from view and object
			App.get_running_app().root.get_screen("main").remove_widget(self.floating_goal_object)
			return True

# -*- coding: UTF-8 -*-
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, ReferenceListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from functools import partial

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
goal_data_path = os.path.join(dir_path, ".goaldata.json")

import json

# Not used at the moment. Will hold main screen and settings screen in the future
class RootWidget(ScreenManager):
	pass

# Holds all the content
class MainScreen(Screen):
	# Holds the GridLayout object that actually contains the satisfaction elements
	content = ObjectProperty()

	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(**kwargs)

		# Check if data has been saved and load if it has
		if os.path.isfile(goal_data_path):
			def temp(*args):
				with open(goal_data_path) as f:
					try:
						tmp = json.load(f)
					except:
						return
				for i in tmp["content"]:
					# i is a dictionary of optional values
					self.content.add_widget(GoalObject(**i))
			Clock.schedule_once(temp)

class MainApp(App):
	def on_stop(self):
		# only save the main info of the GoalObjects, because the representation will change
		# This should include slider value and name, and will probably include color and slider increment in the future
		tmp = {"content": []}

		# iterate over all children of content in reverse order (because you need to add them in reverse order to the list)
		for i in App.get_running_app().root.get_screen("main").content.children:
			tmp["content"].append({"name": i.nameInput.text, "value": i.slider.value})
		tmp["content"].reverse()

		# Write the data to a file
		with open(goal_data_path, 'w') as outfile:
			json.dump(tmp, outfile)

	def on_pause(self):
		self.on_stop()

class GoalMoveArea(Widget):
	touched = BooleanProperty(False)

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
			goal_object = self.parent.parent
			goal_object_copy = GoalObject(value=goal_object.slider.value, name=goal_object.nameInput.text)
			
			scroll_view = goal_object.parent.parent
			Clock.schedule_once(partial(self.scroll_if_necessary, touch, scroll_view))

			# Set correct absolute position and size
			goal_object_copy.pos = goal_object.to_window(goal_object.x, goal_object.y)
			goal_object_copy.size = goal_object.size

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
			goal_object = self.parent.parent
			parent = goal_object.parent
			children = parent.children[:]

			# find position of floating element in its parent
			cur = 0
			for i in range(len(children)):
				if children[i] == goal_object:
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


class GoalObject(BoxLayout):
	# Defined in the kv file. Used to set background color of the widget 
	mainColor = ListProperty([])

	# SipmplisticTextInput object (class defined in kv file).
	nameInput = ObjectProperty(None)

	# The main slider that let's user set his satisfaction
	slider = ObjectProperty(None)

	def __init__(self, **kwargs):
		# value of slider
		value = kwargs.pop("value", 0)
		# Value of goal text
		text = kwargs.pop("name", "")

		super(GoalObject, self).__init__(**kwargs)

		# Set values of widgets once they are initialised
		def tmp(*args):
			self.slider.value = value
			self.nameInput.text = text
		Clock.schedule_once(tmp)

if __name__ == "__main__":
	MainApp().run()


# TODO

# Main part:

# Adjust scrolling speed depending on how close to the edge we are
# Possibly add a way to change the color of individual goals?
# Add subgoals

# Non urgent:

# Add menu
# Make menu have 3 tabs: main, statistics and options
# Statistics can draw graphs
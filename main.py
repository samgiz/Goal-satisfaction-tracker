# -*- coding: UTF-8 -*-
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
goal_data_path = os.path.join(dir_path, ".goaldata.json")

import json

class RootWidget(ScreenManager):
	pass

class MainScreen(Screen):
	content = ObjectProperty()
	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(**kwargs)
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
		with open(goal_data_path, 'w') as outfile:
			json.dump(tmp, outfile)

	def on_pause(self):
		self.on_stop()



class GoalObject(BoxLayout):
	mainColor = ListProperty([])
	nameInput = ObjectProperty(None)
	slider = ObjectProperty(None)
	def __init__(self, **kwargs):
		value = kwargs.pop("value", 0)
		text = kwargs.pop("name", "")
		super(GoalObject, self).__init__(**kwargs)
		def tmp(*args):
			self.slider.value = value
			self.nameInput.text = text
		Clock.schedule_once(tmp)

if __name__ == "__main__":
	MainApp().run()


# TODO

# Main part:

# Add drag and drop functionality
# Add padding around goal
# Fix colours to make it appealing
# Possibly add a way to change the color of individual goals?
# Add subgoals

# Non urgent:

# Add menu
# Make menu have 3 tabs: main, statistics and options
# Statistics can draw graphs
# Can change slider increment in options
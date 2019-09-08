from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from main_screen.goal_object.GoalObject import GoalObject
from kivy.clock import Clock

import os
import json

# Directory of MainScreen.py file
file_dir = os.path.dirname(os.path.realpath(__file__))

# The path of the root directory
root_dir = os.path.dirname(file_dir)

# The path to the user data
goal_data_path = os.path.join(root_dir, ".goaldata.json")

Builder.load_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'MainScreen.kv'))

# Holds all the content
class MainScreen(Screen):
	# Holds the GridLayout object that actually contains the satisfaction elements
	content = ObjectProperty()

	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(**kwargs)

		# Check if data has been saved and load if it has
		# The loading of the data needs to be performed after the widget has been initialized
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
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager
from main_screen.MainScreen import MainScreen

import os
import json

# The path of the root directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# The path to the user data
goal_data_path = os.path.join(dir_path, ".goaldata.json")

# Not used at the moment. Will hold main screen and settings screen in the future
class RootWidget(ScreenManager):
	pass

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
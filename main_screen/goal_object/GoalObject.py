from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from main_screen.goal_object.GoalMoveArea import GoalMoveArea
from kivy.clock import Clock

import os

Builder.load_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'GoalObject.kv'))

# The main object of the main screen. Stores all the info of a single goal / subgoal
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

	# Return a copy of the current object
	def copy(self):
		return GoalObject(value=self.slider.value, name=self.nameInput.text)
# -*- coding: UTF-8 -*-
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, ReferenceListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
goal_data_path = os.path.join(dir_path, ".goaldata.json")

import json

# Not used at the moment. Will hold main screen and settings screen in the future
class RootWidget(ScreenManager):
	pass

# Drag and drop functionality plan
# 1. When a content element is pressed on a certain area, create scatter as follows
# 	 scatter = Scatter(do_rotation=False, do_scale=False, do_translation_x=False)
# 2. Make the initial element transparent
# 3. Whenever the scatter moves, check the mouse position. If the mouse is no longer over the original element, swap elements around until it is
# 4. When releasing scatter, make the element no longer transparent and remove scatter

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
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			# Make element transparent
			touch.grab(self)
			self.touched = True
			self.last_touch = touch.y

			# Create a scatter to hold floating element
			goal_object = self.parent.parent
			goal_object_copy = GoalObject(value=goal_object.slider.value, name=goal_object.nameInput.text)
			
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
			self.floating_goal_object.y += touch.y-self.last_touch
			print(self.floating_goal_object.y)
			self.last_touch = touch.y


	def on_touch_up(self, touch):
		if touch.grab_current is self:
			# Make element no longer transparent
			print(touch)
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

	


class DragVerticalBehavior:
	'''
	The DragBehavior `mixin <https://en.wikipedia.org/wiki/Mixin>`_ provides
	Drag behavior. When combined with a widget, dragging in the rectangle
	defined by :attr:`drag_rectangle` will drag the widget. Please see
	the :mod:`drag behaviors module <kivy.uix.behaviors.drag>` documentation
	for more information.

	.. versionadded:: 1.8.0
	'''

	drag_distance = NumericProperty(0)
	'''Distance to move before dragging the :class:`DragBehavior`, in pixels.
	As soon as the distance has been traveled, the :class:`DragBehavior` will
	start to drag, and no touch event will be dispatched to the children.
	It is advisable that you base this value on the dpi of your target device's
	screen.

	:attr:`drag_distance` is a :class:`~kivy.properties.NumericProperty` and
	defaults to the `scroll_distance` as defined in the user
	:class:`~kivy.config.Config` (20 pixels by default).
	'''

	drag_timeout = NumericProperty(0)
	'''Timeout allowed to trigger the :attr:`drag_distance`, in milliseconds.
	If the user has not moved :attr:`drag_distance` within the timeout,
	dragging will be disabled, and the touch event will be dispatched to the
	children.

	:attr:`drag_timeout` is a :class:`~kivy.properties.NumericProperty` and
	defaults to the `scroll_timeout` as defined in the user
	:class:`~kivy.config.Config` (55 milliseconds by default).
	'''

	drag_rect_x = NumericProperty(0)
	'''X position of the axis aligned bounding rectangle where dragging
	is allowed (in window coordinates).

	:attr:`drag_rect_x` is a :class:`~kivy.properties.NumericProperty` and
	defaults to 0.
	'''

	drag_rect_y = NumericProperty(0)
	'''Y position of the axis aligned bounding rectangle where dragging
	is allowed (in window coordinates).

	:attr:`drag_rect_Y` is a :class:`~kivy.properties.NumericProperty` and
	defaults to 0.
	'''

	drag_rect_width = NumericProperty(100)
	'''Width of the axis aligned bounding rectangle where dragging is allowed.

	:attr:`drag_rect_width` is a :class:`~kivy.properties.NumericProperty` and
	defaults to 100.
	'''

	drag_rect_height = NumericProperty(100)
	'''Height of the axis aligned bounding rectangle where dragging is allowed.

	:attr:`drag_rect_height` is a :class:`~kivy.properties.NumericProperty` and
	defaults to 100.
	'''

	drag_rectangle = ReferenceListProperty(drag_rect_x, drag_rect_y,
										   drag_rect_width, drag_rect_height)
	'''Position and size of the axis aligned bounding rectangle where dragging
	is allowed.

	:attr:`drag_rectangle` is a :class:`~kivy.properties.ReferenceListProperty`
	of (:attr:`drag_rect_x`, :attr:`drag_rect_y`, :attr:`drag_rect_width`,
	:attr:`drag_rect_height`) properties.
	'''

	def __init__(self, **kwargs):
		self._drag_touch = None
		super(DragVerticalBehavior, self).__init__(**kwargs)

	def _get_uid(self, prefix='sv'):
		return '{0}.{1}'.format(prefix, self.uid)

	def on_touch_down(self, touch):
		xx, yy, w, h = self.drag_rectangle
		x, y = touch.pos
		if not self.collide_point(x, y):
			touch.ud[self._get_uid('svavoid')] = True
			return super(DragBehavior, self).on_touch_down(touch)
		if self._drag_touch or ('button' in touch.profile and
								touch.button.startswith('scroll')) or\
				not ((xx < x <= xx + w) and (yy < y <= yy + h)):
			return super(DragBehavior, self).on_touch_down(touch)

		# no mouse scrolling, so the user is going to drag with this touch.
		self._drag_touch = touch
		uid = self._get_uid()
		touch.grab(self)
		touch.ud[uid] = {
			'mode': 'unknown',
			'dx': 0,
			'dy': 0}
		Clock.schedule_once(self._change_touch_mode,
							self.drag_timeout / 1000.)
		return True

	def on_touch_move(self, touch):
		if self._get_uid('svavoid') in touch.ud or\
				self._drag_touch is not touch:
			return super(DragBehavior, self).on_touch_move(touch) or\
				self._get_uid() in touch.ud
		if touch.grab_current is not self:
			return True

		uid = self._get_uid()
		ud = touch.ud[uid]
		mode = ud['mode']
		if mode == 'unknown':
			ud['dx'] += abs(touch.dx)
			ud['dy'] += abs(touch.dy)
			if ud['dx'] > sp(self.drag_distance):
				mode = 'drag'
			if ud['dy'] > sp(self.drag_distance):
				mode = 'drag'
			ud['mode'] = mode
		if mode == 'drag':
			self.x += touch.dx
			self.y += touch.dy
		return True

	def on_touch_up(self, touch):
		if self._get_uid('svavoid') in touch.ud:
			return super(DragBehavior, self).on_touch_up(touch)

		if self._drag_touch and self in [x() for x in touch.grab_list]:
			touch.ungrab(self)
			self._drag_touch = None
			ud = touch.ud[self._get_uid()]
			if ud['mode'] == 'unknown':
				super(DragBehavior, self).on_touch_down(touch)
				Clock.schedule_once(partial(self._do_touch_up, touch), .1)
		else:
			if self._drag_touch is not touch:
				super(DragBehavior, self).on_touch_up(touch)
		return self._get_uid() in touch.ud

	def _do_touch_up(self, touch, *largs):
		super(DragBehavior, self).on_touch_up(touch)
		# don't forget about grab event!
		for x in touch.grab_list[:]:
			touch.grab_list.remove(x)
			x = x()
			if not x:
				continue
			touch.grab_current = x
			super(DragBehavior, self).on_touch_up(touch)
		touch.grab_current = None

	def _change_touch_mode(self, *largs):
		if not self._drag_touch:
			return
		uid = self._get_uid()
		touch = self._drag_touch
		ud = touch.ud[uid]
		if ud['mode'] != 'unknown':
			return
		touch.ungrab(self)
		self._drag_touch = None
		touch.push()
		touch.apply_transform_2d(self.parent.to_widget)
		super(DragBehavior, self).on_touch_down(touch)
		touch.pop()
		return

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
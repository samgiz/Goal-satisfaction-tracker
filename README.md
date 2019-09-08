# Overview

This is a fairly simple application to help track the progress of ones goals. The following functionalities are currently supported:
* Adding goals and setting their percentages
* Reordering the goals using drag  and drop functionality

In the future I plan to add:
* the ability to add subgoals, based on which the cumulative percentage would be calculated
* ability to have different colors for different goals
* additional user options for ease of use
* a separate tab for completed goals (hall of fame)
* possibly some way to track statistics and draw graphs, so that one could check their progress over time

# Setup

You need to have Python 3.5 or higher installed, along with the following libraries:
* Cython
* kivy
* pygame

Assuming you have Python set up, you can simply run `cat requirements.txt | xargs -n 1 -L 1 pip3 install` in order to install the packages. It is important to do it this way and **not** `pip3 install -r requirements.txt`, so that the packages are installed one at a time, since Cython is a prerequisite for Kivy.

Once the installation is complete you may run the app with `python3 main.py` from the root directory.
# shape_animation_dataset.py
# Used to create a dataset of shapes moving on a simple background

# Checklist
#   - Directions
#       - left to right
#       - right to left
#       - top to bottom
#       - bottom to top
#       - diagonal (4 directions)
#   - Shapes
#       - Circle
#       - Rectangle
#       - Triangle (A little more difficult to setup with randomizing)

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import os
import pdb

DATA = os.path.expanduser(os.path.join(os.getcwd(), "GANimation\\shape_data"))

# os.makedirs(os.path.join(DATA, f'circle_right'))
# os.makedirs(os.path.join(DATA, f'circle_left'))
# os.makedirs(os.path.join(DATA, f'circle_up'))
# os.makedirs(os.path.join(DATA, f'circle_down'))

# os.makedirs(os.path.join(DATA, f'rectangle_right'))

i = 0

# Define the animation function to update the position of the patch
def right(frame):
    # Calculate the new position of the patch
    x = x0 + frame * 0.01
    y = y0

    # Save the current frame
    # plt.savefig(f'{DATA}\\circle_right\\circle_right_{i+1}\\circle_right_{i+1}_{frame}.jpg')
    # plt.savefig(f'{DATA}\\rectangle_right_{x}_{y}.jpg')

    # Update the position of the patch
    # patch.set_center((x, y)) # Circle
    patch.set_xy((x, y)) # Rectangle

def left(frame):
    # Calculate the new position of the circle
    x = x0 - frame * 0.01
    y = y0

    # Save the current frame
    plt.savefig(f'{DATA}\\circle_left\\circle_left_{i+1}\\circle_left_{i+1}_{frame}.jpg')
    # plt.savefig(f'{DATA}\\rectangle_right_{x}_{y}.jpg')

    # Update the position of the circle patch
    patch.set_center((x, y))

def up(frame):
    # Calculate the new position of the circle
    x = x0 
    y = y0 + frame * 0.01

    # Save the current frame
    # plt.savefig(f'{DATA}\\circle_up\\circle_up_{i+1}\\circle_up_{i+1}_{frame}.jpg')
    # plt.savefig(f'{DATA}\\rectangle_right_{x}_{y}.jpg')

    # Update the position of the circle patch
    # patch.set_center((x, y))
    patch.set_xy((x, y))

def down(frame):
    # Calculate the new position of the circle
    x = x0
    y = y0 - frame * 0.01

    # Save the current frame
    plt.savefig(f'{DATA}\\circle_down\\circle_down_{i+1}\\circle_down_{i+1}_{frame}.jpg')
    # plt.savefig(f'{DATA}\\rectangle_right_{x}_{y}.jpg')

    # Update the position of the circle patch
    patch.set_center((x, y))

# while i < 100:
# Create a figure and axis with no axis labels or ticks and a black background
fig, ax = plt.subplots() # Default figure size is 6.4 Width by 4.8 Height in inches
# ax.axis('off')
# fig.set_facecolor("black")
# ax.set_facecolor("black")

# Define the initial position of the shapes randomly based on shape and so that it stays in bounds
# Circle
# radius = (random.random() * 0.1) + 0.05  # Radius of the circle (0.05 to 0.15)
# circlemax = 0.36 # Farthest over circle can go (x or y) without going off the board from animation

# Right
# x0, y0 = (random.random() * (circlemax - radius)) + radius, random.random() * (1 - (radius * 2)) + radius

# Left
# x0, y0 = 1 - ((random.random() * (circlemax - radius)) + radius), random.random() * (1 - (radius * 2)) + radius

# Up
# x0, y0 = random.random() * (1 - (radius * 2)) + radius, (random.random() * (circlemax - radius)) + radius

# Down
# x0, y0 = random.random() * (1 - (radius * 2)) + radius, 1 - ((random.random() * (circlemax - radius)) + radius)

# Rectangle
width, height = 0.25, 0.25 # Height and width of the rectangle (MAX 0.25)
rectMax = 0.35 # The farthest over the rectangle can be without going out of bounds
# x0, y0 = random.random() * (1 - width), random.random() * (1 - height)
x0, y0 = 0.25, 0.25

# Create the patch
# patch = plt.Circle((x0, y0), radius, fc='white')
patch = plt.Rectangle((x0, y0), width, height, fc='black')
# patch = plt.Polygon(([(0.1, 0.1), (0.9, 0.1), (0.5, 0.8)]), facecolor='red', edgecolor='black')

# Add the shape to the axis
ax.add_patch(patch)

# Add a folder for the current iteration in shape_data
# results_dir = os.path.join(DATA, f'circle_right\\circle_right_{i+1}')
# results_dir = os.path.join(DATA, f'circle_left\\circle_left_{i+1}')
# results_dir = os.path.join(DATA, f'circle_up\\circle_up_{i+1}')
# results_dir = os.path.join(DATA, f'circle_down\\circle_down_{i+1}')
# os.makedirs(results_dir)

# Create animation objects
# moveright = animation.FuncAnimation(fig, right, frames=50, interval=50, repeat=False, blit=False)
# moveleft = animation.FuncAnimation(fig, left, frames=50, interval=50, repeat=False, blit=False)
moveup = animation.FuncAnimation(fig, up, frames=50, interval=50, repeat=False, blit=False)
# movedown = animation.FuncAnimation(fig, down, frames=50, interval=50, repeat=False, blit=False)

# Save the animation as a gif
# moveright.save(f'{DATA}\\circle_right\\circle_right_{i+1}\\circle_right_anim_{i+1}.gif', fps=25)
# moveleft.save(f'{DATA}\\circle_left\\circle_left_{i+1}\\circle_left_anim_{i+1}.gif', fps=25)
# moveup.save(f'{DATA}\\circle_up\\circle_up_{i+1}\\circle_up_anim_{i+1}.gif', fps=25)
# movedown.save(f'{DATA}\\circle_down\\circle_down_{i+1}\\circle_down_anim_{i+1}.gif', fps=25)

i += 1

plt.show()
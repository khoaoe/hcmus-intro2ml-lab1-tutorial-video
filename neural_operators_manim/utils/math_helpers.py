# utils/math_helpers.py
from manim import *

def create_discrete_vector(num_dots=10, color=BLUE, radius=0.1, spacing=0.3):
    """Creates a 1D array of dots representing a flattened finite-dimensional vector."""
    dots = VGroup(*[Dot(radius=radius, color=color) for _ in range(num_dots)])
    dots.arrange(RIGHT, buff=spacing)
    return dots
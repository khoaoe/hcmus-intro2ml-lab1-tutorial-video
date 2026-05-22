from manim import config


def apply_global_config():
    """Apply project-wide render config for silent Manim scene files."""
    config.background_color = "#0B1020"
    config.frame_width = 16
    config.frame_height = 9
    config.frame_rate = 20


BG = "#0B1020"
CARD_BG = "#111827"
GRID = "#2A3346"
TEXT = "#E5E7EB"
MUTED = "#9CA3AF"

INPUT = "#38BDF8"
OUTPUT = "#34D399"
OPERATOR = "#FBBF24"
WARNING = "#FB7185"
PURPLE = "#A78BFA"
NVIDIA_GREEN = "#76B900"


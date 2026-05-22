from manim import config


# ---------------------------------------------------------------------
# Global render configuration
# ---------------------------------------------------------------------

def apply_global_config():
    """
    Apply project-wide Manim config.

    Call this once at the top of every scene file, before Scene classes.
    Programmatic config keeps rendering consistent even when scene files
    live in nested folders.
    """
    config.background_color = "#0B1020"
    config.frame_width = 16
    config.frame_height = 9
    config.frame_rate = 20


# ---------------------------------------------------------------------
# Project palette
# ---------------------------------------------------------------------

BG = "#0B1020"
CARD_BG = "#111827"
GRID = "#2A3346"
TEXT = "#E5E7EB"
MUTED = "#9CA3AF"

INPUT = "#38BDF8"      # blue/teal
OUTPUT = "#34D399"     # green
OPERATOR = "#FBBF24"   # yellow
WARNING = "#FB7185"    # red-pink
PURPLE = "#A78BFA"

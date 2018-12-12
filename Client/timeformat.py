"""Module to set the desired Time Format to display."""

from datetime import datetime

def get_time_format(gui):
    """Return the desired Time Format."""
    return datetime.now().strftime(gui.res.time_format)

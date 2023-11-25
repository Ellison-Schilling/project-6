"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
from acp_times import open_time
from acp_times import close_time
import arrow
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

start = arrow.get("2012-01-01T00:00")

def test_zero_input():
    """
    Testing the minimum valid input
    """
    assert (open_time(0, 200, start) == start)
    assert (close_time(0, 200, start) == start.replace(hour=+ 1))

    assert (open_time(0, 300, start) == start)
    assert (close_time(0, 300, start) == start.replace(hour=+ 1))
    
    assert (open_time(0, 400, start) == start)
    assert (close_time(0, 400, start) == start.replace(hour=+ 1))

    assert (open_time(0, 600, start) == start)
    assert (close_time(0, 600, start) == start.replace(hour=+ 1))

    assert (open_time(0, 1000, start) == start)
    assert (close_time(0, 1000, start) == start.replace(hour=+ 1))

def test_equal_input():
    """
    Testing the maximum valid input
    """
    assert (open_time(200,200,start) == start.replace(hour=+5, minute=+53))
    assert (close_time(200,200, start) == start.replace(hour=+13, minute=+30))

    assert (open_time(300, 300, start) == start.replace(hour=+9))
    assert (close_time(300, 300, start) == start.replace(hour=+20))

    assert (open_time(400, 400, start) == start.replace(hour=+12, minute=+8))

def test_max_input():
    """
    Testing the maximum valid input
    """
    assert (open_time(240, 200, start)  == start.replace(hour=+5, minute=+53))
    assert (close_time(240, 200, start) == start.replace(hour=+13, minute=+30))
    
    assert (open_time(360, 300, start) == start.replace(hour=+9))
    assert (close_time(360, 300, start) == start.replace(hour=+20))

    assert (open_time(480, 400, start) == start.replace(hour=+12, minute=+8))
 
def test_over_input():
    """
    Testing above the maximum valid input
    """
    assert (open_time(100000, 200, start) is None)
    assert (close_time(100000, 200, start) is None)
    
    assert (open_time(100000, 300, start) is None)
    assert (close_time(100000, 300, start) is None)

    assert (open_time(100000, 400, start) is None)
    assert (close_time(100000, 400, start) is None)

    assert (open_time(100000, 600, start) is None)
    assert (close_time(100000, 600, start) is None)

    assert (open_time(100000, 1000, start) is None)
    assert (close_time(100000, 1000, start) is None)


def test_negative_control_input():
    """
    Assuring negative numbers as controls yield Nones
    """
    assert (open_time(-100, 200, start) is None)
    assert (close_time(-100, 200, start) is None)
    
    assert (open_time(-100, 300, start) is None)
    assert (close_time(-100, 300, start) is None)

    assert (open_time(-100, 400, start) is None)
    assert (close_time(-100, 400, start) is None)

    assert (open_time(-100, 600, start) is None)
    assert (close_time(-100, 600, start) is None)

    assert (open_time(-100, 1000, start) is None)
    assert (close_time(-100, 1000, start) is None)
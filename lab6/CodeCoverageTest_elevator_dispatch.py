import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---------- door_action ----------
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"


def test_overload():
    assert door_action(700, False, False) == "overload"


def test_blocked_reopens():
    assert door_action(100, True, False) == "reopen"


def test_normal_close():
    assert door_action(100, False, False) == "close"


# ---------- next_direction ----------
def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


def test_up_continues_up():
    assert next_direction(3, "up", [5]) == "up"


def test_up_reverses_down():
    assert next_direction(5, "up", [2]) == "down"


def test_down_continues_down():
    assert next_direction(5, "down", [2]) == "down"


def test_down_reverses_up():
    assert next_direction(2, "down", [5]) == "up"


def test_idle_goes_up():
    assert next_direction(3, "idle", [7]) == "up"


def test_idle_goes_down():
    assert next_direction(3, "idle", [1]) == "down"


# ---------- pick_elevator ----------
def test_pick_elevator_closest_idle():
    cars = [("A", 1, True), ("B", 4, True)]
    assert pick_elevator(cars, 5) == "B"

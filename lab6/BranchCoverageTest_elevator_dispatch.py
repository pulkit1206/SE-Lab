import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ================= door_action : every decision True AND False =================
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"          # emergency T

def test_emergency_beats_overload_and_block():
    assert door_action(900, True, True) == "hold_open"           # emergency wins

def test_overload():
    assert door_action(700, False, False) == "overload"          # emergency F, load>630 T

def test_overload_beats_blocked():
    assert door_action(700, True, False) == "overload"

def test_load_exactly_at_limit_is_not_overload():
    assert door_action(630, False, False) == "close"             # boundary: 630 > 630 F

def test_load_just_over_limit_is_overload():
    assert door_action(631, False, False) == "overload"          # boundary

def test_blocked_reopens():
    assert door_action(100, True, False) == "reopen"             # blocked T

def test_normal_close():
    assert door_action(100, False, False) == "close"             # blocked F


# ================= next_direction : direction == "up" =================
def test_up_with_requests_above():
    assert next_direction(3, "up", [5]) == "up"

def test_up_nothing_above_but_below():
    assert next_direction(5, "up", [2]) == "down"

def test_up_no_requests():
    assert next_direction(5, "up", []) == "idle"

def test_up_request_on_current_floor_only():
    assert next_direction(5, "up", [5]) == "idle"                # neither above nor below

# ================= next_direction : direction == "down" =================
def test_down_with_requests_below():
    assert next_direction(5, "down", [2]) == "down"

def test_down_nothing_below_but_above():
    assert next_direction(2, "down", [5]) == "up"

def test_down_no_requests():
    assert next_direction(5, "down", []) == "idle"

# ================= next_direction : idle / any other direction =================
def test_idle_goes_up():
    assert next_direction(3, "idle", [7]) == "up"

def test_idle_goes_down():
    assert next_direction(3, "idle", [1]) == "down"

def test_idle_no_requests():
    assert next_direction(3, "idle", []) == "idle"

def test_idle_prefers_up_when_both_sides():
    assert next_direction(3, "idle", [1, 9]) == "up"

def test_up_prefers_up_when_both_sides():
    assert next_direction(3, "up", [1, 9]) == "up"

def test_down_prefers_down_when_both_sides():
    assert next_direction(3, "down", [1, 9]) == "down"

def test_unknown_direction_treated_like_idle():
    assert next_direction(3, "sideways", [9]) == "up"


# ================= pick_elevator =================
def test_pick_elevator_no_cars_returns_none():
    assert pick_elevator([], 4) is None                          # loop never runs

def test_pick_elevator_single_car():
    assert pick_elevator([("A", 1, True)], 4) == "A"             # best is None -> True

def test_pick_elevator_closest_idle():
    cars = [("A", 1, True), ("B", 4, True)]
    assert pick_elevator(cars, 5) == "B"                         # gap < best_gap True

def test_pick_elevator_later_car_farther_is_ignored():
    cars = [("A", 4, True), ("B", 1, True)]
    assert pick_elevator(cars, 5) == "A"                         # gap < best_gap False

def test_pick_elevator_busy_penalty_applied():
    cars = [("A", 5, False), ("B", 8, True)]                     # A: 0+5=5, B: 3
    assert pick_elevator(cars, 5) == "B"

def test_pick_elevator_busy_but_much_closer_still_wins():
    cars = [("A", 5, False), ("B", 20, True)]                    # A: 5, B: 15
    assert pick_elevator(cars, 5) == "A"

def test_pick_elevator_tie_keeps_first():
    cars = [("A", 3, True), ("B", 7, True)]                      # both gap 2
    assert pick_elevator(cars, 5) == "A"

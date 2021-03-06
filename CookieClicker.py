"""
Cookie Clicker Simulator
"""

import simpleplot
# import SimpleGUICS2Pygame.simpleplot as simpleplot
# Used to increase the timeout, if necessary
# import SimpleGUICS2Pygame.codeskulptor as codeskulptor
import codeskulptor

codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

import math

# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + str(self._time) + ", Current cookies: " + str(self._current_cookies) \
               + ", CPS: " + str(self._cps) + ", Total cookies: " + str(self._total_cookies)

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        diff = cookies - self._current_cookies
        if diff <= 0:
            return 0.0
        else:
            return math.ceil(diff / self._cps)

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._time += time
            self._current_cookies += self._cps * time
            self._total_cookies += self._cps * time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_cookies:
            self._current_cookies -= cost
            self._cps += additional_cps
            self._history.append((self._time, item_name, cost, self._total_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    my_bi = build_info.clone()
    my_cs = ClickerState()
    while my_cs.get_time() <= duration:
        item_name = strategy(my_cs.get_cookies(), my_cs.get_cps(), duration - my_cs.get_time(), my_bi)
        if item_name is None:
            break
        time_to_wait = my_cs.time_until(my_bi.get_cost(item_name))
        if my_cs.get_time() + time_to_wait > duration:
            break
        my_cs.wait(time_to_wait)
        my_cs.buy_item(item_name, my_bi.get_cost(item_name), my_bi.get_cps(item_name))
        my_bi.update_item(item_name)
    my_cs.wait(duration - my_cs.get_time())
    return my_cs


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"


def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always return the cheapest item you can afford in the time left
    """
    item_name = None
    best_cost = None
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost > cookies + cps * time_left:
            continue
        if best_cost is None or item_cost < best_cost:
            item_name = item
            best_cost = item_cost
    return item_name


def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always return the most expensive item you can afford in the time left
    """
    item_name = None
    best_cost = None
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost > cookies + cps * time_left:
            continue
        if best_cost is None or item_cost > best_cost:
            item_name = item
            best_cost = item_cost
    return item_name


def strategy_best(cookies, cps, time_left, build_info):
    """
    Always return the best item you can afford in the time left
    """
    item_name = None
    best_ratio = None
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost > cookies + cps * time_left:
            continue
        item_ratio = build_info.get_cps(item) / item_cost
        if best_ratio is None or item_ratio > best_ratio:
            item_name = item
            best_ratio = item_ratio
    return item_name


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print(strategy_name, ":", state)

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)


run()

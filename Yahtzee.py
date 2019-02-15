"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

import poc_holds_testsuite

# Used to increase the timeout, if necessary
try:
    import codeskulptor
except:
    import SimpleGUICS2Pygame.codeskulptor as codeskulptor
codeskulptor.set_timeout(50)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = {()}
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """

    max_value = 0
    for num in hand:
        value = hand.count(num) * num
        if value > max_value:
            max_value = value
    return max_value


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    total_score = 0.0
    all_outcomes = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    for roll in all_outcomes:
        possible_hand = list(held_dice)
        for die in roll:
            possible_hand.append(die)
        total_score += score(possible_hand)
    return total_score / len(all_outcomes)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    all_sequences = {()}
    for die in hand:
        temp_set = set()
        for partial_sequence in all_sequences:
            new_sequence = list(partial_sequence)
            new_sequence.append(die)
            temp_set.add(tuple(new_sequence))
        all_sequences = all_sequences.union(temp_set)
    sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
    return set(sorted_sequences)


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """

    expected_score = 0.0
    hold_dice = ()
    all_holds = gen_all_holds(hand)
    for hold in all_holds:
        value = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if value > expected_score:
            expected_score = value
            hold_dice = hold
    return expected_score, hold_dice


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print("Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score)


run_example()
poc_holds_testsuite.run_suite(gen_all_holds)

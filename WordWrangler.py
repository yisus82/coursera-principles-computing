"""
Student code for Word Wrangler game
"""

from urllib.request import urlopen

try:
    import codeskulptor
except:
    import SimpleGUICS2Pygame.codeskulptor as codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    for element in list1:
        if element not in new_list:
            new_list.append(element)

    return new_list


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_list = []
    for element in list1:
        if element in list2:
            new_list.append(element)

    return new_list


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    new_list = []
    idx1 = 0
    idx2 = 0
    while idx1 < len(list1) and idx2 < len(list2):
        if list1[idx1] <= list2[idx2]:
            new_list.append(list1[idx1])
            idx1 += 1
        else:
            new_list.append(list2[idx2])
            idx2 += 1
    if idx1 == len(list1):
        for element in list2[idx2:]:
            new_list.append(element)
    else:
        for element in list1[idx1:]:
            new_list.append(element)

    return new_list


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1

    middle = int(len(list1) / 2)
    return merge(merge_sort(list1[:middle]), merge_sort(list1[middle:]))


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    new_strings = []
    for string in rest_strings:
        for idx in range(len(string) + 1):
            new_strings.append(string[:idx] + first + string[idx:])

    return rest_strings + new_strings


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urlopen(url).read().decode('utf-8').strip()
    words = netfile.split("\n")
    return words


def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)


# Uncomment when you are ready to try the game
run()

"""
Create constants that cannot be altered
"""
import collections


def define(**names_values):
    """
    Defines a set of constants. Example usage:

        COLOR = define(RED='0xff0000', GREEN='0x00ff00', BLUE='0x0000ff')
        background = COLOR.BLUE
        print(background)  # output: 0x0000ff

    :param names_values: pairs of names and values for each constants
    :return: A set of constants, see example usage above
    """
    blue_print = collections.namedtuple("const", names_values)
    const = blue_print(**names_values)
    return const

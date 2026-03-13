"""
Example code that contains a class.
"""

def testsub():
    print("This is my subroutine")

class myclass:
    """
    This class takes a number upon initialisation.
    It is able to print this number later.
    """
    def __init__(self, num=3):
        """
        Initialize the class.
        """
        self.num = 3

    def print_num(self):
        """
        Print the number.
        """
        print("The number is %i"%self.num)

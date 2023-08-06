'''

*************************************************************************************************************************************************************

                                                                       WELCOME TO CONSOLEBAR

Stunning progress bars for consoles for showing progress of python loops!

A Python Module for creating beautiful
progress bar for showing progress of 
python loops (for, while, etc.).

Useful especially for huge loops which
take loads of time to execute.

@params

loop_to_execute (Required): Python loop parameter (list(), dictionary(), tuple(), str(), range(), etc.) i.e. iterable object for which progress bar is shown.
prefix (Optional): A string which is shown before the progress bar to describe the progress bar (Default: "Progress:").
suffix (Optional): A string which is shown after the progress bar to describe the progress percentage shown after the progress bar (Default: "Complete").
length (Optional): Length of the progress bar in charecters. Can be adjusted according to one's console charecter width (Default: 50).

This module is made and intended for non-commercial use only.

© Abhay Tripathi

*************************************************************************************************************************************************************

'''

from __future__ import print_function

class ConsoleBar:

    def __init__(self, loop_to_execute, prefix = "Progress:", suffix = "Complete", length = 50):
        self.decimals = 1
        self.loop_to_execute = loop_to_execute
        self.length = length
        self.fill = "\u2588"
        self.prefix = prefix
        self.suffix = suffix
        self.number_of_iterations = len(loop_to_execute)

    def __iter__(self):
        self.print_bar(0)
        for iteration_number, item in enumerate(self.loop_to_execute):
            yield item
            self.print_bar(iteration_number + 1)
        print()

    def print_bar(self, iteration):
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (iteration / float(self.number_of_iterations)))
        filledLength = int(self.length * iteration // self.number_of_iterations)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f"\r{self.prefix} |{bar}| {percent}% {self.suffix}", end = "\r")

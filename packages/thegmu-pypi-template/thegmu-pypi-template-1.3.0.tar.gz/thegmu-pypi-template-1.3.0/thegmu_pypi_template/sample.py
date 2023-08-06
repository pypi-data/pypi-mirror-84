# -*- coding: utf-8 -*-
"""

    sample.py
    ~~~~~~~~~

    Sample module provided for testing purposes.

"""


class Sample():
    """Sample object for pytest."""

    @staticmethod
    def hello(name="The GMU Project"):
        """This sample function returns a string of "Hello 'name'".

        :param name: A optional string for hello testing.

        """

        return("Hello %s" % (name, ))

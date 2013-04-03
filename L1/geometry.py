# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 17:24:53 2013

@author: mansmagnusson
"""
def area(radius):
    """
    >>> area(1)
    3.141592653589793
    >>> area(-1)
    None!
    """
    from math import pi
    if radius<0:
        print "None!"
    else:        
        return radius**2*pi


def RectangleArea(base,height):
    """
    >>> RectangleArea(3,2)
    6
    """
    return base*height

def Triangle(base,height):
    """
    >>> Triange(2,1)
    1
    """
    return base*height/2


if __name__ == "__main__":
    import doctest
    doctest.testmod()

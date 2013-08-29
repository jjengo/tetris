# Author: Jonathan Jengo

ScreenSize = (480, 450)

# Represents a [x,y] coordinate
class Point:
    
    # Initialize
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Set the [x,y] point
    def set(self, x, y):
        self.x = x
        self.y = y
        
    # Move the point by delta
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
        
    # Return [x,y] as a tuple
    def tuple(self):
        return (self.x, self.y)
        
# Represents a size abstraction
class Dimension:
    
    # Inifialize
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    # Set the dimension size
    def set(self, width, height):
        self.width = width
        self.height = height
        
    # Return rotated dimensions
    def rotate(self):
        return Dimension(self.height, self.width)
        
    # Return the dimension as a tuple
    def tuple(self):
        return (self.width, self.height)
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
import sympy as sp

### basic Fin Calculations
R = 5 # max radius of the envelope (SET FORM OTHER PARAMETERS)


h = int(input("Enter the height of the fin (from centerline) > envelope radius or 0:"))
# a = input("Enter the angle of the fin (degrees): ")
b = int(input("Enter the base of the fin > 0:"))
t = int(input("Enter the length of the fin tip > 0 or base: "))

# sanity check the inputs
if h < 0:
    print("Height cannot be negative")
    h = input("Enter the height of the fin (from centerline) > envelope radius or 0:")
elif h <= R:
    print ("Height is equal to envelope radius.")
    height_checkinput = input("Proceed? (y/n): ")
    if height_checkinput != 'n':
        h = R   
        print("Height set to inital entry.")
    else:
        h = input("Enter the height of the fin (from centerline) > envelope radius or 0:")
else:
    print ("Fin height is good!")

##### TO DO: check if the fin tip is greater than the fin base

### Create points for the surface path


### Create NACA 0012 airfoil points/spline
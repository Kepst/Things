'''
use another way to color the image
get the tick value right
?use pygame to be possible to zoom?
'''

import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyder as diff
from numpy.polynomial.polynomial import polyval as val
import numpy as np
import time

SIZE = 1000  # setting the size of the image, it will be SIZE x SIZE


def solve(poly, start, err=10**-5, maxiter=100):
    """
    finds a polynomial root using Newton's method
    :param poly: tuple with the coefficients of the polynomial
    :param start: first value to use the newton method
    :param err: minimum difference between each iteration before stopping
    :param maxiter: maximum number of iterations before stopping
    :return: value of the root found
    """
    x = start
    xn = start + 1
    iter = 1
    while (abs(x - xn) > err).any() and iter < maxiter:
        print(iter)
        iter += 1
        x = xn
        v = val(x, poly)
        d = val(x, (diff(poly)))
        xn = x - v/d
    return x


p = (2, 2, 1, 3j, -1, 1)  # sets the polynomial coefficients
minr = float("inf")
maxr = float("-inf")
mini = float("inf")
maxi = float("-inf")
roots = np.roots(p[::-1])  # np.roots uses the inverse order than the rest... why?
for v in roots:
    print(v, abs(v))
    minr = min(v.real, minr)
    maxr = max(v.real, maxr)
    mini = min(v.imag, mini)
    maxi = max(v.imag, maxi)

minr -= 1
maxr += 1
mini -= 1
maxi += 1

xx = np.linspace(minr, maxr, num=SIZE)
yy = np.linspace(mini, maxi, num=SIZE)

#zz = val(xx, p)
#plt.plot(xx, zz)
#plt.show()

zz = []  # create and populate the image vector
l = 0
for nx in xx:
    l += 1
    nz = []
    for ny in yy*1j:
        nz.append(nx+ny)
    zz.append(np.array(nz))

zz = np.array(zz).T  # transpose so the imaginary value is the y axis
t = time.time()
zz = solve(p, zz)
print(time.time() - t)  # time the creation of the image


plt.imshow(abs(zz))  # show the image
plt.show()
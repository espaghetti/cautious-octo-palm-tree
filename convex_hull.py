import math
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))
import numpy as np
import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

	# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False
		
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)
		
	def eraseHull(self,polygon):
		self.view.clearLines(polygon)
		
	def showText(self,text):
		self.view.displayStatusText(text)

# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	# time complexity: O(nlog(n))
	# space complexity: O(n)
	def compute_hull(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert(type(points) == list and type(points[0]) == QPointF)

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		# sort(points by x-value) (sort by the first value of the tuple)
		list.sort(points, key=lambda point: point.x())  # O(nlog(n))
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		# polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		final_hull = self.find_hull(points)             # O(nlog(n))

		polygon = [QLineF(final_hull[i].x(), final_hull[i].y(),
						 final_hull[(i + 1) % len(final_hull)].x(), final_hull[(i + 1) % len(final_hull)].y())
				   for i in range(len(final_hull))]     # O(k) --do it for each point in the polygon (less than the total points)
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

	# divide into subset--leftSet is points/2 (ceiling of)
	# rightmost is size of points/2 (floor of)
	# recursively call this function until points/2 < 1
	# time complexity: O(nlog(n))
	# space complexity: O(n) -- store all points still, just in left and right halves
	def find_hull(self, points):
		length = len(points)   # c
		if length == 1:        # c
			return points      # c
		elif length == 2:      # c
			return points      # c
		elif length == 3:      # c
			# find the hull of 3
			# find starting point, get decreasing slopes
			slopeP0ToP1 = (points[1].y() - points[0].y()) / (points[1].x() - points[0].x())   # c
			slopeP0ToP2 = (points[2].y() - points[0].y()) / (points[2].x() - points[0].x())   # c
			if slopeP0ToP1 > slopeP0ToP2:  # c
				return points              # c
			else:
				# make it clockwise oriented
				temp = [0, 0, 0]   # c
				new2 = points[2]   # c
				new1 = points[1]   # c
				new = points[0]    # c
				temp[0] = new      # c
				temp[1] = new2     # c
				temp[2] = new1     # c
				return temp        # c
		# separate hull into left and right parts (left will be larger if odd)
		left_hull = points[:math.ceil(length / 2)]     # c
		right_hull = points[math.ceil(length / 2):]    # c
		# recursively solve the sub hulls
		L = self.find_hull(left_hull)                  # O(log(n)) *  O(n) (find tangents, and do half the points)
		R = self.find_hull(right_hull)                 # O(log(n)) *  O(n) (find tangents, and do half the points)
		# find the upper and lower tangents of the two hulls
		upper_tangent = self.find_upper_tangent(L, R)                        # O(n)
		lower_tangent = self.find_lower_tangent(L, R)                        # O(n)
		# MERGE HULLS
		final_hull = self.merge_hull(L, R, upper_tangent, lower_tangent)     # O(n)
		return final_hull                                                    # c

	# merge the two hull parts together
	# time complexity: O(n) -- n is the number of points in L and R because
		# it is running the for/while loops at worse case, number of points in L/R times
	# space complexity: O(n) -- create the new array with size 2n (drop constant 2)
	def merge_hull(self, L, R, upper_tangent, lower_tangent):
		# start at L[0]
		# find upper_tangent left point
		# find upper_tangent right point
		# connect those/ put upper right point in the list
		# add points to final_hull until we get to right lower tangent
		upper_left_point = upper_tangent.pointAt(0)     # c
		upper_right_point = upper_tangent.pointAt(1)    # c
		lower_right_point = lower_tangent.pointAt(1)    # c
		lower_left_point = lower_tangent.pointAt(0)     # c

		final_hull = [L[0]]                             # c
		for point in L:                                 # O(n) where n is the number of points in L
			# if we don't already have the upper left tangent point, add the rest of points til we find it
			# then add the upper left tangent
			if L[0] == upper_left_point:                # c
				break                                   # c
			elif point == upper_left_point:             # c
				final_hull.append(point)                # c
				break                                   # c
			elif point != upper_left_point and point != L[0]:    # c
				final_hull.append(point)                # c
			elif point == L[0]:                         # c
				continue                                # c
			else:
				break                                   # c
		index = 0
		# find the index of the next point to add
		while upper_right_point != R[index]:            # while loop: O(n) where n is the number of points in R
			index += 1                                  # c
		for i in range(index, len(R)):                  # O(n) where n is the number of points in R
			if R[i] == upper_right_point:
				# if the upper right tangent point == lower right tangent point, we don't want to add them twice
				if upper_right_point == lower_right_point:   # c
					break
				final_hull.append(upper_right_point)         # c
				continue
			elif R[i] != lower_right_point:             # c
				final_hull.append(R[i])                 # c
			elif R[i] == lower_right_point:             # c
				break
			else:
				break
		final_hull.append(lower_right_point)            # c
		final_hull.append(lower_left_point)             # c
		# after we add the rest of the tangent points, add the rest of the points until we get back to the beginning
		index = 0
		while lower_left_point != L[index]:             # while loop: O(n) where n is the number of points in L
			index += 1                                  # c
		for i in range(index, len(L)):                  # for loop: O(n) where n is the number of points in L
			if L[i] != lower_left_point:                # c
				final_hull.append(L[i])                 # c
			elif L[i] == L[0]:                          # c
				break                                   # c
		final_hull.append(L[0])                         # c
		return final_hull                               # c

	# find the line that forms the upper tangent
	# time complexity: O(n)
	# space complexity: O(1)
	def find_upper_tangent(self, L, R):
		# find rightmost point rightmost_left_point in L and leftmost point leftmost_right_point in R
		index_L = self.get_most_right_point_index(L)                   # O(n) -- tc of the function
		rightmost_left_point = L[index_L]                              # c
		index_R = 0  # -1??                                            # c
		leftmost_right_point = R[index_R]                              # c
		temp = QLineF(rightmost_left_point, leftmost_right_point)      # c
		done = 0                                                       # c
		# run until we find upper tangent
		while not done:                                                # O(n) -> O(n/2) + O(n/2)
			done = 1                                                   # c
			temp = QLineF(rightmost_left_point, leftmost_right_point)    # c
			if abs(index_L) > len(L):                                  # c
				index_L = index_L + len(L)                             # c
			# find the point that makes the slope more negative
			while abs(index_L) < len(L):                               # O(n/2)  -- run only points in  L, which is half of them
				old_index_L = index_L                                  # c
				index_L = index_L - 1                                  # c
				if abs(index_L) > len(L):                              # c
					index_L = index_L + (len(L) - 1)                   # c
				# r is point we check
				r = L[index_L]                                         # c
				prev_slope = self.calc_slope(leftmost_right_point, rightmost_left_point)   # c
				slope = self.calc_slope(leftmost_right_point, r)       # c
				# if the slope is steeper (so higher up the hull)
				if slope <= prev_slope:                                # c
					rightmost_left_point = r                           # c
					temp = QLineF(r, leftmost_right_point)             # c
					done = 0                                           # c
				else:                                                  # c
					# otherwise, make no changes to point rightmost_left_point
					index_L = old_index_L                              # c
					done = 1                                           # c
					break                                              # c
			# move right hull point up to correct point
			while abs(index_R) < (len(R) - 1):                         # O(n/2) -- check only points in R, which is half of them
				prev_slope = self.calc_slope(leftmost_right_point, rightmost_left_point)   # c
				old_index_R = index_R                                  # c
				index_R = index_R + 1                                  # c
				r = R[index_R]                                         # c
				slope = self.calc_slope(rightmost_left_point, r)       # c
				if slope > prev_slope:                                 # c
					done = 0                                           # c
					leftmost_right_point = r                           # c
					temp = QLineF(rightmost_left_point, r)             # c
					break                                              # c
				else:                                                  # c
					index_R = old_index_R                              # c
					done = 1                                           # c
					break                                              # c
		return temp                                                    # c

	# find the line that forms the lower tangent
	# time complexity: O(n^3)
	# space complexity: O(1)
	def find_lower_tangent(self, L, R):
		# find rightmost point p in L and leftmost point q in R
		index_L = self.get_most_right_point_index(L)                   # O(n) -- tc of the function
		rightmost_left_point = L[index_L]                              # c
		index_R = 0                                                    # c
		leftmost_right_point = R[index_R]                              # c
		temp = QLineF(rightmost_left_point, leftmost_right_point)      # c
		done = 0                                                       # c
		# while we still haven't found the lower tangent
		while not done:                                               # O(n) -- we will check each point at most once
			done = 1                                                   # c
			temp = QLineF(rightmost_left_point, leftmost_right_point)   # c
			if index_L == (len(L)):                                    # c
				index_L = 0                                            # c
			# find upper lower left point of lower tangent
			while abs(index_L) < (len(L)):                             # O(n/2) -- we will check only half the points at most
				# set index_L = index of current right_most_left_point of L + 1
				old_index_L = index_L                                  # c
				index_L = index_L + 1                                  # c
				if index_L == (len(L)):                                # c
					index_L = 0                                        # c
				# r is point we check
				r = L[index_L]                                         # c
				prev_slope = self.calc_slope(leftmost_right_point, rightmost_left_point)   # c
				slope = self.calc_slope(leftmost_right_point, r)       # c
				# if the slope is steeper (so higher up the hull)
				if slope > prev_slope:                                 # c
					rightmost_left_point = r                           # c
					temp = QLineF(r, leftmost_right_point)             # c
					done = 0                                           # c
				else:                                                  # c
					# otherwise, make no changes to point rightmost_left_point
					index_L = old_index_L                              # c
					done = 1                                           # c
					break                                              # c
			# find right point of lower tangent
			while abs(index_R) < (len(R)):                             # O(n/2) -- we will check only half the points at a time
				prev_slope = self.calc_slope(leftmost_right_point, rightmost_left_point)  # c
				old_index_R = index_R                                  # c
				index_R = index_R - 1                                  # c
				r = R[index_R]                                         # c
				slope = self.calc_slope(rightmost_left_point, r)       # c
				# if the point moves the line down, make that the new point
				if slope <= prev_slope:                                # c
					done = 0                                           # c
					leftmost_right_point = r                           # c
					temp = QLineF(rightmost_left_point, r)             # c
					break                                              # c
				else:                                                  # c
					index_R = old_index_R                              # c
					done = 1                                           # c
					break                                              # c
		return temp                                                    # c

	# find the slope
	# time complexity: O(1)
	# space complexity: O(1) -- no new memory allocated
	def calc_slope(self, p1, p2):
		return (p1.y()-p2.y()) / (p1.x() - p2.x())    # O(1)

	# find the point that is most right relative to the rest of the left sub-hull
	# time complexity: O(n) -- run for loop n times, and other operations are constant time
	# space complexity: O(1)
	def get_most_right_point_index(self, L):
		most_right_point = L[0]                        # c
		index_of_most_right_point = 0                  # c
		for index in range(len(L)):                    # O(n) -- n is num points in L
			if L[index].x() > most_right_point.x():    # c
				most_right_point = L[index]            # c
				index_of_most_right_point = index      # c
		return index_of_most_right_point               # c

	# find the index of where the point is in the sub-hull
	# time complexity: O(n) -- run the for loop at most n times
	# space complexity: O(1)
	def get_index_of_point(self, Hull, point):
		for index in range(len(Hull)):                 # O(n) -- n is num points in Hull
			if Hull[index] == point:                   # c
				return index                           # c

#import self
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
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

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
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		# sort(points by x-value) (sort by the first value of the tuple)
		list.sort(points, key=lambda point: point.x())  # O(nlog(n))
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		#polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		#print("before find_hull")
		new_points = self.find_hull(points)
		#print("after find_hull")
		#print(new_points)
		polygon = [QLineF(new_points[i].x(), new_points[i].y(),
						 new_points[(i + 1) % len(new_points)].x(), new_points[(i + 1) % len(new_points)].y())
				   for i in range(len(new_points))]
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

	# divide into subset--leftSet is points/2 (ceiling of)
	# rightmost is size of points/2 (floor of)
	# recursively call this function until points/2 < 1
	# lol then combine the hulls XD simple
	def find_hull(self, points):
		length = len(points)

		if length == 1:
			return points

		elif length == 2:
			return points

		elif length == 3:
			# find the hull of 3
			# find starting point, get decreasing slopes
			slopeP0ToP1 = (points[1].y() - points[0].y()) / (points[1].x() - points[0].x())
			slopeP0ToP2 = (points[2].y() - points[0].y()) / (points[2].x() - points[0].x())
			if slopeP0ToP1 > slopeP0ToP2:
				return points
			else:
				# make it clockwise oriented
				temp = [0, 0, 0]
				new2 = points[2]
				new1 = points[1]
				new = points[0]
				temp[0] = new
				temp[1] = new2
				temp[2] = new1
				return temp
		left_hull = points[:math.ceil(length / 2)]
		right_hull = points[math.ceil(length / 2):]
		L = self.find_hull(left_hull)
		R = self.find_hull(right_hull)

		print("L  ", L)
		print("R  ", R)
		upper_tangent = self.find_upper_tangent(L, R)
		print("upper tangent  ", upper_tangent)
		lower_tangent = self.find_lower_tangent(L, R)
		# MERGE HULLS
		final_hull = self.merge_hull(L, R, upper_tangent, lower_tangent)
		# points = points + [upper_tangent.pointAt(0)] + [upper_tangent.pointAt(1)]
		return final_hull

	def merge_hull(self, L, R, upper_tangent, lower_tangent):
		# start at L[0]
		# find upper_tangent left point
		# find upper_tangent right point
		# connect those/ put upper right point in the list
		# add points to final_hull until we get to right lower tangent
		upper_left_point = upper_tangent.pointAt(0)
		upper_right_point = upper_tangent.pointAt(1)
		lower_right_point = lower_tangent.pointAt(1)
		lower_left_point = lower_tangent.pointAt(0)

		final_hull = []
		final_hull.append(L[0])
		for point in L:
			# if we don't already have the upper left tangent point, add the rest of points til we find it
			# then add the upper left tangent
			if L[0] == upper_left_point:
				break
			elif point == upper_left_point:
				final_hull.append(point)
				break
			elif point != upper_left_point and point != L[0]:
				final_hull.append(point)
			elif point == L[0]:
				continue
			else:
				break
		index = 0
		while upper_right_point != R[index]:
			index += 1
		for i in range(index, len(R)):
			if R[i] == upper_right_point:
				#if the upper right tangent point == lower right tangent point, we don't want to add them twice
				if upper_right_point == lower_right_point:
					break
				final_hull.append(upper_right_point)
				continue
			elif R[i] != lower_right_point:
				final_hull.append(R[i])
			elif R[i] == lower_right_point:
				break
			else:
				break
		final_hull.append(lower_right_point)
		#if lower_right_point != lower_left_point:
		final_hull.append(lower_left_point)
		index = 0
		while lower_left_point != L[index]:
			index += 1
		for i in range(index, len(L)):
			if L[i] != lower_left_point:
				final_hull.append(L[i])
			else:
				break
		final_hull.append(L[0])
		return final_hull

# right in the list to go clockwise
	def find_upper_tangent(self, L, R):
		# find rightmost point rightmost_left_point in L and leftmost point leftmost_right_point in R
		index_L = self.get_most_right_point_index(L)
		rightmost_left_point = L[index_L]
		index_R = 0  # -1??
		leftmost_right_point = R[index_R]
		temp = QLineF(rightmost_left_point, leftmost_right_point)
		done = 0
		old_index_L = 0
		while not done:
			done = 1
			temp = QLineF(rightmost_left_point, leftmost_right_point)
			if abs(index_L) > len(L):
				index_L = index_L + len(L)
			while abs(index_L) < len(L):
				old_index_L = index_L
				index_L = index_L - 1
				if abs(index_L) > len(L):
					index_L = index_L + (len(L) - 1)
				r = L[index_L]  # r is point we check, L is left hull
				prev_slope = self.calc_slope(leftmost_right_point, rightmost_left_point)
				slope = self.calc_slope(leftmost_right_point, r)
				# if the slope is steeper (so higher up the hull)
				if slope <= prev_slope:
					rightmost_left_point = r
					temp = QLineF(r, leftmost_right_point)
					done = 0
					#if abs(index_L) > len(L):
						#index_L = index_L + 3
					#index_L = old_index_L
					#break
				else:
					# otherwise, make no changes to point rightmost_left_point
					index_L = old_index_L
					done = 1
					break
			# move right hull point up to correct point
			while abs(index_R) < (len(R) - 1):
				prev_slope = self.calc_slope(leftmost_right_point, rightmost_left_point)
				old_index_R = index_R
				index_R = index_R + 1
				r = R[index_R]
				slope = self.calc_slope(rightmost_left_point, r)
				if slope > prev_slope:
					done = 0
					leftmost_right_point = r
					temp = QLineF(rightmost_left_point, r)
					break
				else:
					index_R = old_index_R
					done = 1
					break

		return temp

	def find_lower_tangent(self, L, R):
		# find rightmost point p in L and leftmost point q in R
		# temp = line(p,q)
		index_L = self.get_most_right_point_index(L)
		rightmost_left_point = L[index_L]
		index_R = 0
		leftmost_right_point = R[index_R]
		temp = QLineF(rightmost_left_point, leftmost_right_point)
		done = 0
		while not done:
			done = 1
			temp = QLineF(rightmost_left_point, leftmost_right_point)
			if index_L == (len(L)):
				index_L = 0
			while abs(index_L) < (len(L)):
				# set index_L = index of current right_most_left_point of L + 1
				old_index_L = index_L
				index_L = index_L + 1
				if index_L == (len(L)):
					index_L = 0
				r = L[index_L]  # r is point we check, L is left hull
				prev_slope = self.calc_slope(leftmost_right_point, rightmost_left_point)
				slope = self.calc_slope(leftmost_right_point, r)
				# if the slope is steeper (so higher up the hull)
				if slope > prev_slope:
					rightmost_left_point = r
					temp = QLineF(r, leftmost_right_point)
					done = 0
					#MAYBE DELETE
					#break
				else:
					# otherwise, make no changes to point rightmost_left_point
					index_L = old_index_L
					done = 1
					break
			# move right hull point up to correct point
			while abs(index_R) < (len(R)):
				prev_slope = self.calc_slope(leftmost_right_point, rightmost_left_point)
				old_index_R = index_R
				index_R = index_R - 1
				r = R[index_R]
				slope = self.calc_slope(rightmost_left_point, r)
				if slope <= prev_slope:
					done = 0
					leftmost_right_point = r
					temp = QLineF(rightmost_left_point, r)
					# MAYBE DELETE
					break
				else:
					index_R = old_index_R
					done = 1
					break
		print("lower tangent: ", temp)
		return temp

	def calc_slope(self, p1, p2):
		return (p1.y()-p2.y()) / (p1.x() - p2.x())

	def get_most_right_point_index(self, L):
		most_right_point = L[0]
		index_of_most_right_point = 0
		for index in range(len(L)):
			if L[index].x() > most_right_point.x():
				most_right_point = L[index]
				index_of_most_right_point = index
		return index_of_most_right_point

	def get_index_of_point(self, Hull, point):
		for index in range(len(Hull)):
			if Hull[index] == point:
				return index


#if __name__ == '__main__':
	#ConvexHullSolver.compute_hull(self,points=[QPointF(0, 0), QPointF(1, 1), QPointF(2, 1)], pause=False, view=False)
	#new_points = ConvexHullSolver.find_hull(self, points=[QPointF(0, 0), QPointF(1, 1), QPointF(2, 1)])

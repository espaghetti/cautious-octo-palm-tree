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
		polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER

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
		l = len(points)
		temp = []
		if l == 1:
			return points

		if l == 2:
			# find the hull of 2
			# check the slope
			slope = (points[1].y() - points[0].y()) / (points[1].x() - points[0].y())
			if slope >= 0:
				return points
			elif slope < 0:
				temp[0] = points[1]
				temp[1] = points[0]
				return temp
			return points

		if l == 3:
			# find the hull of 3
			# find starting point, get decreasing slopes
			p = points[0]
			slopeP0ToP1 = (points[1].y() - points[0].y()) / (points[1].x() - points[0].y())
			slopeP0ToP2 = (points[2].y() - points[0].y()) / (points[2].x() - points[0].y())
			if slopeP0ToP1 > slopeP0ToP2:
				return points
			else:
				# make it clockwise oriented
				temp[0] = points[0]
				temp[1] = points[2]
				temp[2] = points[1]
				return temp

			return points

		return

# right in the list to go clockwise
	def find_upper_tangent(self, L, R):
		#find rightmost point p in L and leftmost point q in R
		#temp = line(p,q)
		done = 0
		while not done:
			done = 1
			# while temp is not upper tangent to L:
				# r = p's counter clockwise neighbor
				# temp = line(r,q)
				# p = r
				# done = 0
			# while temp is not upper tangent to R:
				# r = q's clockwise neighbor
				# temp = line(p,r)
				# q = r
				# done = 0
			#return temp
			return 0

	def find_lower_tangent(self, L, R):
		# find rightmost point p in L and leftmost point q in R
		# temp = line(p,q)
		done = 0
		while not done:
			done = 1
			# while temp is not upper tangent to L:
				# r = p's counter counterclockwise neighbor
				# temp = line(r,q)
				# p = r
				# done = 0
			# while temp is not upper tangent to R:
				# r = q's counterclockwise neighbor
				# temp = line(p,r)
				# q = r
				# done = 0
		# return temp
		return 0


# if __name__ == '__main__':
	# find_hull(points =  )

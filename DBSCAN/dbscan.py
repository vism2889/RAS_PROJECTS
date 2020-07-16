#! /usr/bin/env python
# AUTHOR: Morgan Visnesky
# DATE: 07/15/2020
# FILENAME: dbscan.py
#
###############################################################################
# INFO: DBSCAN with visualizer
#
# References:
# - https://medium.com/nearist-ai/dbscan-clustering-tutorial-dd6a9b637a4b
# - https://en.wikipedia.org/wiki/DBSCAN
#
###############################################################################
import random


class Point(object):
    # holds information about point
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.label = None
        self.neighbors = []

class DB(object):
    def __init__(self, numClusters, pointsPerCluster):
        self.clusters = numClusters
        self.pointsPer = pointsPerCluster
        self.allPoints = []

    def makeCluster(self, minx, miny, minz, maxx, maxy, maxz):
        # generates coordinates for points in clusters

        # noisey data points
        for i in range(self.clusters):
            for j in range(self.pointsPer):
                x = random.randint(minx*(i+1),maxx*(i+7))
                y = random.randint(minx*(i+1),maxx*(i+1))
                z = random.randint(minx*(i+1)+7*i,maxx*(i+1))
                point = Point(x,y,z)
                self.allPoints.append(point)

        '''
        # clean data points in shape of cubes
        for m in range(10):
            for i in range(maxx-2):
                for j in range(maxy-2):
                    for k in range(0,10,2):
                        x = i
                        y = j
                        z = k
                        point = Point(x+m*10,y+m*10,z+m*10)
                        self.allPoints.append(point)
        '''

def distFunc(point1, point2):
    dist = (((point2.x-point1.x)**2)+((point2.y-point1.y)**2)+((point2.z-point1.z)**2))**0.5
    return dist

def regionQuery(D, P, eps):
    """
    Find all points in dataset `D` within distance `eps` of point `P`.

    This function calculates the distance between a point P and every other
    point in the dataset, and then returns only those points which are within a
    threshold distance `eps`.
    """
    neighbors = []
    for Pn in range(0, len(D)):
        if distFunc(D[P],D[Pn]) < eps:
           neighbors.append(Pn)

    return neighbors

def growCluster(D, labels, P, C, eps, MinPts):
    """
    Grow a new cluster with label `C` from the seed point `P`.

    This function searches through the dataset to find all points that belong
    to this new cluster. When this function returns, cluster `C` is complete.

    Parameters:
      `D`      - The dataset (a list of vectors)
      `labels` - List storing the cluster labels for all dataset points
      `P`      - Index of the seed point for this new cluster
      `C`      - The label for this new cluster.
      `eps`    - Threshold distance
      `MinPts` - Minimum required number of neighbors
    """

    # SearchQueue is a FIFO queue of points to evaluate. It will only ever
    # contain points which belong to cluster C (and have already been labeled
    # as such).
    #
    # The points are represented by their index values (not the actual vector).
    #
    # The FIFO queue behavior is accomplished by appending new points to the
    # end of the list, and using a while-loop rather than a for-loop.
    SearchQueue = [P]

    # For each point in the queue:
    #   1. Determine whether it is a branch or a leaf
    #   2. For branch points, add their unclaimed neighbors to the search queue
    i = 0
    while i < len(SearchQueue):

        # Get the next point from the queue.
        P = SearchQueue[i]

        # Find all the neighbors of P
        NeighborPts = regionQuery(D, P, eps)

        # If the number of neighbors is below the minimum, then this is a leaf
        # point and we move to the next point in the queue.
        if len(NeighborPts) < MinPts:
            i += 1
            continue

        # Otherwise, we have the minimum number of neighbors, and this is a
        # branch point.

        # For each of the neighbors...
        for Pn in NeighborPts:

            # If Pn was labelled NOISE during the seed search, then we
            # know it's not a branch point (it doesn't have enough
            # neighbors), so make it a leaf point of cluster C and move on.
            if labels[Pn] == -1:
               labels[Pn] = C
            # Otherwise, if Pn isn't already claimed, claim it as part of
            # C and add it to the search queue.
            elif labels[Pn] == 0:
                # Add Pn to cluster C.
                labels[Pn] = C

                # Add Pn to the SearchQueue.
                SearchQueue.append(Pn)

        # Advance to the next point in the FIFO queue.
        i += 1

def MyDBSCAN(D, eps, MinPts):
    """
    Cluster the dataset `D` using the DBSCAN algorithm.

    MyDBSCAN takes a dataset `D` (a list of vectors), a threshold distance
    `eps`, and a required number of points `MinPts`.

    It will return a list of cluster labels. The label -1 means noise, and then
    the clusters are numbered starting from 1.
    """

    # This list will hold the final cluster assignment for each point in D.
    # There are two reserved values:
    #    -1 - Indicates a noise point
    #     0 - Means the point hasn't been considered yet.
    # Initially all labels are 0.
    labels = [0]*len(D)

    # C is the ID of the current cluster.
    C = 0

    # This outer loop is just responsible for picking new seed points--a point
    # from which to grow a new cluster.
    # Once a valid seed point is found, a new cluster is created, and the
    # cluster growth is all handled by the 'expandCluster' routine.

    # For each point P in the Dataset D...
    # ('P' is the index of the datapoint, rather than the datapoint itself.)
    for P in range(0, len(D)):

        # Only points that have not already been claimed can be picked as new
        # seed points.
        # If the point's label is not 0, continue to the next point.
        if not (labels[P] == 0):
           continue

        # Find all of P's neighboring points.
        NeighborPts = regionQuery(D, P, eps)

        # If the number is below MinPts, this point is noise.
        # This is the only condition under which a point is labeled
        # NOISE--when it's not a valid seed point. A NOISE point may later
        # be picked up by another cluster as a boundary point (this is the only
        # condition under which a cluster label can change--from NOISE to
        # something else).
        if len(NeighborPts) < MinPts:
            labels[P] = -1
        # Otherwise, if there are at least MinPts nearby, use this point as the
        # seed for a new cluster.
        else:
           # Get the next cluster label.
           C += 1

           # Assing the label to our seed point.
           labels[P] = C

           # Grow the cluster from the seed point.
           growCluster(D, labels, P, C, eps, MinPts)

    # All data has been clustered!
    return labels

db = DB(5,50)
db.makeCluster(1,1,1,7,7,7)
#print(db.allPoints)
#one = Point(1,1,1)
#two = Point(5,5,5)
#print(distFunc(one, two))

clusterLabelList = MyDBSCAN(db.allPoints,2.5,3)
#print(clusterLabelList)

import matplotlib.pyplot as plt
fig = plt.figure("Morgans DBSCAN")
ax = plt.axes(projection='3d')


red = (1,0,0,1)
green = (0,1,0,1)
blue = (0,0,1,1)
yellow = (0.5,0.5,0,1)
#black = (0,0,0,1)
colors =[red,green,blue,yellow]
for i in range(len(clusterLabelList)):
    colors.append((random.random(),random.random(),random.random(),1))
for i in range(len(db.allPoints)):
    x,y,z = (db.allPoints[i].x,db.allPoints[i].y,db.allPoints[i].z)
    clust = clusterLabelList[i]
    if clust != -1:
        # colors and displays points in clusters
        color = tuple(colors[clusterLabelList[i]])
        ax.plot3D(x, y,z, 'o', markerfacecolor=color, markeredgecolor='k', markersize=6)
    else:
        # colors and displays noise points
        color = tuple((0,0,0,1))
        ax.plot3D(x, y,z, 'o', markerfacecolor=color, markeredgecolor='k', markersize=1)


#plt.legend(loc="upper left")



plt.title('Estimated number of clusters: %d' % max(clusterLabelList))
plt.show()

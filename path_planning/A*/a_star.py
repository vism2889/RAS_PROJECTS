#! /usr/bin/env python
# AUTHOR: Morgan Visnesky
# DATE: 07/10/2020
# FILENAME: a_star.py
#
###############################################################################
# INFO: A* search algorithm with pygame visualizer
#
# References:
# - Daniel Shiffman's 'Coding Train': https://www.youtube.com/watch?v=aKYlikFAV4k (parts 1-3)
# - Wikipedia https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
#
###############################################################################


import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys
from pygame.locals import *
import math
import random


class Node(object):
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None

        # creates barriers
        if (random.random() < 0.4):
            self.wall = True
        else:
            self.wall = False

    def addNeighbors(self,nodeMap, cols, rows):
        i = self.x
        j = self.y
        # sides
        if i < (cols -1):
            self.neighbors.append(nodeMap[i+1][j])
        if i > 0:
            self.neighbors.append(nodeMap[i-1][j])
        if j < (rows-1):
            self.neighbors.append(nodeMap[i][j+1])
        if j > 0:
            self.neighbors.append(nodeMap[i][j-1])

        # diagonals
        if i > 0 and j > 0:
            self.neighbors.append(nodeMap[i-1][j-1])
        if i < cols-1 and j > 0:
            self.neighbors.append(nodeMap[i+1][j-1])
        if i > 0 and j < rows-1:
            self.neighbors.append(nodeMap[i-1][j+1])
        if i < cols-1 and j < rows-1:
            self.neighbors.append(nodeMap[i+1][j+1])


class Map(object):
    # Holds functions to build 2D map list + draw map and map labels
    def __init__(self):
        self.map = []
        self.ROWS = 0
        self.COLS = 0
        self.DISPLAY = ''
        self.rowHeight = 0
        self.colWidth = 0
        self.margin = 0
        self.gridColor = ''
        self.textColor = ''
        self.nodeMap = []

    def mapp(self, ROWS, COLS):
        self.ROWS = ROWS
        self.COLS = COLS
        map = []
        for i in range(ROWS):
            newRow = []
            for j in range(COLS):
                newRow.append(0)
            map.append(newRow)
        self.map = map
        return self.map

    def drawMap(self, DISPLAY,rowHeight, colWidth, margin, gridColor):
        self.DISPLAY = DISPLAY
        self.rowHeight = rowHeight
        self.colWidth = colWidth
        self.margin = margin
        self.gridColor = gridColor
        for i in range(self.ROWS):
            for j in range(self.COLS):
                pygame.draw.rect(DISPLAY,gridColor,(i*colWidth+margin,margin+j*rowHeight,colWidth,rowHeight), 1)

    def mapText(self,textColor):
        self.textColor = textColor
        for i in range(self.COLS):
            for j in range(self.ROWS):
                font_obj = pygame.font.Font('freesansbold.ttf', 32)
                #text_surface_obj = font_obj.render(str(math.floor((i**2+j**2)**0.5)), True, GREEN, BLUE)
                text_surface_obj = font_obj.render(str(self.map[i][j]), True, self.textColor, self.gridColor)
                text_rect_obj = text_surface_obj.get_rect()
                text_rect_obj.center = (self.colWidth*i+self.colWidth/2+self.margin, self.rowHeight*j+self.rowHeight/2+self.margin)
                self.DISPLAY.blit(text_surface_obj, text_rect_obj)

    def mapNodes(self):
        nodeMap = []
        for i in range(self.ROWS):
            newRow = []
            for j in range(self.COLS):
                newNode = Node(i,j)
                newRow.append(newNode)
            nodeMap.append(newRow)
        self.nodeMap = nodeMap

        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.nodeMap[i][j].addNeighbors(self.nodeMap,self.COLS, self.ROWS)



openSet = []
closedSet = []
start = ''
end = ''


def heuristic(a,b):
    dist = math.sqrt((b.x - a.x)**2 + (b.y - a.y)**2)
    #dist = abs(a.x-b.x) + abs(a.y-b.y)
    return dist


def main():
    size = 50
    pygame.init()
    pygame.display.set_caption('Morgan\'s A* Planner')
    clock = pygame.time.Clock()
    margin = 10
    display_width = 700
    display_height = 700
    DISPLAY=pygame.display.set_mode((display_width,display_height),0,32)
    colWidth = (display_width - margin*2)//(size)
    rowHeight = (display_height - margin*2)//(size)
    numCols = int((display_width)//colWidth)
    numRows = int((display_height)//rowHeight)
    WHITE=(255,255,255)
    BLUE=(0,0,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    person_x = margin #numCols*colWidth+margin
    person_y = (numRows-1)*rowHeight+margin

    # call map class
    MAP = Map()
    map = MAP.mapp(numRows, numCols)
    #map[1][4] = 'H' #add value
    #print(map)
    DISPLAY.fill(WHITE)
    MAP.mapNodes()
    nodeMap = MAP.nodeMap
    #print('nodemap: ',nodeMap)


    start = nodeMap[0][0]
    end = nodeMap[numCols-1][numRows-1]
    start.wall = False
    end.wall = False
    path = []
    openSet.append(start)
    current = ''
    finished = False
    print('Starting A* Planner: Start = ',start.x,start.y, ' End = ', end.x,end.y)


    MAP.drawMap(DISPLAY, rowHeight, colWidth, margin, BLUE)
    # Animation Loop
    #clock.tick(40)
    while True:
        path = []

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        if len(openSet) > 0:
            # keep going
            lowestIndex = 0
            for i in range(len(openSet)):
                if openSet[i].f < openSet[lowestIndex].f:
                    lowestIndex = i

            current = openSet[lowestIndex]
            if current == end:
                print('A* DONE')
                path.append(end)
                pygame.draw.rect(DISPLAY,BLUE,(end.x*colWidth+margin, end.y*rowHeight+margin,colWidth,rowHeight), 0)
                for i in range(len(openSet)-1):
                    openSet.pop()
                for i in range(len(closedSet)-1):
                    closedSet.pop()

                finished = True

            if finished == False:
                DISPLAY.fill(WHITE)
                temp = current
                path.append(temp)
                while temp.previous != None:
                    path.append(temp.previous)
                    temp = temp.previous


                openSet.remove(current)
                closedSet.append(current)
                neighbors = current.neighbors

                for i in range(len(neighbors)):
                    neighbor = neighbors[i]
                    newPath = False
                    if neighbor not in closedSet and neighbor.wall == False:
                        tempG = current.g + 1
                        if neighbor in openSet:
                            if tempG <= neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                                neighbor.previous = current
                        else:
                            neighbor.g = tempG
                            newPath = True
                            neighbor.previous = current
                            openSet.append(neighbor)
                    if newPath == True:
                        neighbor.h = heuristic(neighbor, end)
                        neighbor.f = neighbor.g + neighbor.h

                    for i in range(len(closedSet)):
                        pygame.draw.rect(DISPLAY,RED,(closedSet[i].x*colWidth+margin, closedSet[i].y*rowHeight+margin,colWidth,rowHeight), 0)
                        #pygame.draw.circle(DISPLAY, RED, (int(closedSet[i].x*colWidth+margin+colWidth/2),int(closedSet[i].y*rowHeight+margin+rowHeight/2)), 6)


                    for i in range(len(openSet)):
                        pygame.draw.rect(DISPLAY,GREEN,(openSet[i].x*colWidth+margin, openSet[i].y*rowHeight+margin,colWidth,rowHeight), 0)
                        #pygame.draw.circle(DISPLAY, GREEN, (int(openSet[i].x*colWidth+margin+colWidth/2),int(openSet[i].y*rowHeight+margin+rowHeight/2)), 6)

                    for i in range(len(path)):
                        pygame.draw.rect(DISPLAY,BLUE,(path[i].x*colWidth+margin, path[i].y*rowHeight+margin,colWidth,rowHeight), 0)
                        #pygame.draw.circle(DISPLAY, BLUE, (int(path[i].x*colWidth+margin+colWidth/2),int(path[i].y*rowHeight+margin+rowHeight/2)), 6)

                    MAP.drawMap(DISPLAY, rowHeight, colWidth, margin, (200,200,200))

                    # path line
                    for i in range(len(path)):
                        if path[i].x == 0 and path[i].y == 0:
                            pygame.draw.line(DISPLAY, (255,205,0), (path[i].x*colWidth+margin+colWidth/2, path[i].y*rowHeight+margin+rowHeight/2), (path[i].x*colWidth+margin+colWidth/2, path[i].y*rowHeight+margin+rowHeight/2), 4)
                        else:
                            pygame.draw.line(DISPLAY, (255,205,0), (path[i].x*colWidth+margin+colWidth/2, path[i].y*rowHeight+margin+rowHeight/2), (path[i+1].x*colWidth+margin+colWidth/2, path[i+1].y*rowHeight+margin+rowHeight/2), 6)



        else:
            print('No Solution')
            break
            # no solution
            
        # obstacles
        for i in range(len(nodeMap)):
            for j in range(len(nodeMap[i])):
                if nodeMap[i][j].wall == True:
                    pygame.draw.rect(DISPLAY,(0,0,0),(nodeMap[i][j].x*colWidth+margin, nodeMap[i][j].y*rowHeight+margin,colWidth,rowHeight), 0)
                    #pygame.draw.circle(DISPLAY, (0,0,0), (int(nodeMap[i][j].x*colWidth+margin+colWidth/2),int(nodeMap[i][j].y*rowHeight+margin+rowHeight/2)), 6)


        # end point
        pygame.draw.rect(DISPLAY,(0,150,150),(end.x*colWidth+margin, end.y*rowHeight+margin,colWidth,rowHeight), 0)
        pygame.draw.circle(DISPLAY, (255,205,0), (int(end.x*colWidth+margin+colWidth/2),int(end.y*rowHeight+margin+rowHeight/2)), 6)

        '''
        pygame.draw.rect(DISPLAY,RED,(person_x,person_y,colWidth,rowHeight), 0)
        person_x += colWidth
        person_y -= rowHeight
        '''
        pygame.display.update()


main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-04-14 14:57:35
# @Author  : Tom Brandherm (s_brandherm19@stud.hwr-berlin.de)
# @Link    : link
# @Version : 0.0.1
"""
Class for analysing the shape of a random number and position of found points.
"""
# =========================================================================== #
#  Copyright 2021 Team Awesome
# =========================================================================== #
#  All Rights Reserved.
#  The information contained herein is confidential property of Team Awesome.
#  The use, copying, transfer or disclosure of such information is prohibited
#  except by express written agreement with Team Awesome.
# =========================================================================== #

# =========================================================================== #
#  SECTION: Imports                                                           
# =========================================================================== #
# standard:
import numpy as np
import math
# local:
import StraightLineEquation as sle
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
# find nearest neighbour, but exclude same point
MINIMAL_DISTANCE = 100
# amount of red dots in one horizantal line 
DOTS_IN_LINE = 6

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class Grid(object):
    """
    Grid of coordinates
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, coordinates:dict):
        # dict of tuples with (x,y)
        self.__coordiantes = coordinates
        # totoal numer of found points
        self.__knots = len(coordinates)
        # calculate the distances from each point to each point
        self.__distances = self.__calculate_distances()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def get_coordinates(self):
        return self.__coordiantes

    def get_knots(self):
        return self.__knots

    def set_coordinates(self, coordinates):
        self.__coordiantes = coordinates

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def find_rectangles(self)->dict:
        """
        Find the corners of every rectangle on the game board.

        Returns
        -------
        dict
            dictionay of lists of corner points for each found rectangle
        """
        # FIRST STEP:
        # Fill the matrix with all the found points in the correct order
        # each element represents one row on the game board
        matrix = [[], [], []]
        for i in range(3):
            # start point
            first_key = list(self.__coordiantes.keys())[0]
            point1 = self.__coordiantes[first_key]
            # find closest point and get the distance
            point2, distance = self.__find_nearest_neighbour(first_key)
            # defining a error range for y values 
            yErr = distance * 0.2
            # use point 1 and 2 to create a straight line equation
            g = sle.StraightLineEquation(point1, point2)
            # check which points are in line with point 1 and 2
            pattern = g.check_points(self.__coordiantes, yErr)
            # fill matching points into the matrix row and delete
            # these for the next iteration
            rest = dict()
            for j, value in enumerate(pattern):
                point = self.__coordiantes[first_key + j]
                if value:
                    matrix[i].append(point)
                else:
                    rest[first_key + j] = point
            self.__coordiantes = rest
            # delete or calculate single missing/double points
            matrix[i] = self.__clean_row(matrix[i], g)
        # SECOND STEP:
        # Iterate through the (3x6) matrix to sort the points to 
        # corners of rectangles
        rectangles = dict()
        for j in range(2):
            for i in range(DOTS_IN_LINE-1):
                rectangle = list()
                rectangle.append(matrix[j+1][i+1])
                rectangle.append(matrix[j][i+1])
                rectangle.append(matrix[j][i])
                rectangle.append(matrix[j+1][i])
                
                rectangles[i+5*j] = rectangle

        return rectangles
        
        
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __convert_dict(self):
        """convert the dict values into a matrix (numpy array)
        Returns
        -------
        [numpy array]
            numpy array of the dict values
        """
        result = self.__coordiantes.values()
        data = list(result)
        return np.array(data)
            
    def __calculate_angle(self, vec1, vec2):
        """calculate the angle between two sensors in degree

        Parameters
        ----------
        vec1 : [1D numpy array]
            vector
        vec2 : [1D numpy array]
            vector

        Returns
        -------
        [float]
            angle between the two vectors
        """
        unit_vector_vec1 = vec1/np.linalg.norm(vec1)
        unit_vector_vec2 = vec2/np.linalg.norm(vec2)
        dot_product = np.dot(unit_vector_vec1, unit_vector_vec2)
        return math.degrees(np.arccos(dot_product))
   
      
    def __calculate_distances(self):
        """calculate the distance between every point and save it into a distance matrix D

        Returns
        -------
        [2D numpy array]
            distance matrix:
                        vec1                vec2            ...     vecn
                vec1    0               d(vec1, vec2)       ...     d(vec1,vecn)
                vec2    d(vec1, vec2)       0               ...     d(vec2,vecn)
                ...     ...                 ...             ...       ...
                vecn    d(vecn, vec1)   d(vecn,vec2)        ...     0
        """
        n = self.__knots
        #reshape matrix to iterable array, every row represents the x and y coordinate of a red dot
        matrix = self.__convert_dict().reshape(n, 2)
        #distance matrix
        D = np.zeros((n,n))
        for i, vector1 in enumerate(matrix):
            for j, vector2 in enumerate(matrix):
                #euclidean distance between two vectors
                if i != j:
                    dist = np.linalg.norm(vector1-vector2)
                    D[i,j] = dist
        return D
  
    
    def __calculate_angles(self):
        """calculate the angle between every point and save it into a angle matrix A

        Returns
        -------
        [2D numpy array]
            distance matrix:
                        vec1                vec2            ...     vecn
                vec1    0               a(vec1, vec2)       ...     a(vec1,vecn)
                vec2    a(vec1, vec2)       0               ...     a(vec2,vecn)
                ...     ...                 ...             ...      ...
                vecn    a(vecn, vec1)   a(vecn,vec2)        ...     0
        """
        n = self.__knots
        #reshape matrix to iterable array, every row represents the x and y coordinate of a red dot
        matrix = self.__convert_dict().reshape(n, 2)
        #angle matrix
        A = np.zeros((n, n))
        for i, vector1 in enumerate(matrix):
            for j, vector2 in enumerate(matrix):
                #angle between two vectors, unnecessary for same vectors
                if i != j:
                    angle = self.__calculate_angle(vector1, vector2)
                    A[i, j] = angle
        return A
 
            
    def __find_nearest_neighbour(self,referencePointKey:tuple)->tuple:
        """
        find nearest neighbour point of a reference point
        Parameters
        ----------
        referencePointKey : tuple
            (x,y)

        Returns
        -------
        tuple
            nearest neighbour (x,y) , distance between reference point and that neighbour
        """
        D = self.__distances
        row = D[referencePointKey]
        hrow = self.__delete_not_horizotals(referencePointKey, row)
        sorted_row = np.sort(hrow)
        for value in sorted_row:
            if value >= MINIMAL_DISTANCE:
                minval = value
                break
        index = np.argwhere(row == minval)[0][0]
        return self.__coordiantes[index], minval
        
        
    def __delete_not_horizotals(self, referencePointKey:tuple, row:list)->list:
        """
        set the distance of every point that is not "horizontal" to zero 

        Parameters
        ----------
        referencePointKey : tuple
            (x,y))
        row : list
            list of distances

        Returns
        -------
        list
            refreshed list of distances
        """
        yRef = self.__coordiantes[referencePointKey][1]
        yMin = yRef-MINIMAL_DISTANCE
        yMax = yRef+MINIMAL_DISTANCE
        for key in self.__coordiantes:
            value = self.__coordiantes[key]
            y = value[1]
            in_between = yMin <= y and y <= yMax
            if not in_between:
                row[key]=0
        return row
    
    
    def __delete_doubles(self, row:list)->list:
        """
        delete double recognized points by chekcing if a second one is close the it

        Parameters
        ----------
        row : list
            list of points in one horizontal line

        Returns
        -------
        list
            list of points in one horizontal line without doubles
        """
        cleaned_row = list()
        upperX = 0
        lowerX = 0
        for coord in row:
            x = coord[0]
            in_between = lowerX <= x and x <= upperX
            if not in_between:
                cleaned_row.append(coord)   
            upperX = x+ MINIMAL_DISTANCE
            lowerX = x - MINIMAL_DISTANCE
        return cleaned_row 
            
            
    def __calculate_missing(self, row:list, g:sle):
        #TODO calculate missing points by using the straight line equation
        # and the known distances
        pass


    def __clean_row(self, row: list, g: sle)->list:
        """
        be sure that the exact number of points are in line
        Parameters
        ----------
        row : list
            list of points in one line
        g : sle
            straight line equation that describes the position

        Returns
        -------
        list
            list of exact 6 equidistant points
        """
        #sort the coords descending by the x value
        row.sort(reverse=True)
        row = self.__delete_doubles(row)
        if len(row) < DOTS_IN_LINE:
            row = self.__calculate_missing(row, g)
        elif len(row) == DOTS_IN_LINE:
            return row
        print("Something went wrong during the data cleaning")
                
# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    pass



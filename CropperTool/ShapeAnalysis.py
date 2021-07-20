#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-04-14 14:57:35
# @Author  : Tom Brandherm (s_brandherm19@stud.hwr-berlin.de)
# @Link    : link
# @Version : 1.0.2
# @Python  : 2.7.0
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
# get float division for python 2.7
from __future__ import division

import numpy as np
import math
import decimal

from numpy.core import numeric
from numpy.core.defchararray import upper

# local:
import StraightLineEquation as sle
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
# find nearest neighbour, but exclude same points (100 is a good fitting value!!)
MINIMAL_DISTANCE = 100
# amount of red dots in one horizantal line 
DOTS_IN_LINE = 6

  
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

    def __init__(self, center, coordinates):
        self.image_center = np.asarray(center)
        # dict of tuples with (x,y)
        self.__coordiantes = self.__clustering(coordinates)
        # total number of found points
        self.__knots = len(coordinates)
        # corners
        self.corners = self.__sort_corners()
        

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def get_coordinates(self):
        return self.__coordiantes

    def get_knots(self):
        return self.__knots

    def set_coordinates(self, coordinates):
        self.__coordiantes = self.__clustering(coordinates)
        self.corners = self.__sort_corners()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def find_rectangles(self):
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
        matrix = self.__calculate_missing_knots()
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
    
    
    def __clustering(self, coords):
        """
        Cluster the coordinates by the distance. Are two ore more coordinates
        in a radial distance range of the given minimal distance there a forming
        one cluster. 

        Parameters
        ----------
        coords : list
            list of points

        Returns
        -------
        dict
            dict of four corner coordintates
        """
        coords_list = list(coords.values())
        cluster = dict()
        new_coords = list()
        key_counter = 0
        while coords_list:
            key_counter += 1
            cluster[key_counter] = list()
            for i, coord in enumerate(coords_list):
                if i == 0:
                    cluster[key_counter].append(coord)
                else:
                    vector1 = np.asarray(cluster[key_counter][0])
                    vector2 = np.asarray(coord)
                    dist = np.linalg.norm(vector1-vector2)
                    if dist < MINIMAL_DISTANCE:
                        cluster[key_counter].append(coord)
                    else:
                        new_coords.append(coord)
            coords_list=new_coords
            new_coords = []
            # calculating the mean of the x and the y value of all coordinates
            # in one cluster. the result is one statistical center point
            cluster[key_counter] = self.__find_center(cluster[key_counter])
        cluster = self.__delete_wrong_detected_cluster(cluster)
        return cluster
    
    
    def __delete_wrong_detected_cluster(self, cluster):
        """
        If more than 4 clusters are found, the "middle" clusters are removed.

        Parameters
        ----------
        cluster : dict
            cluster with a potential lenght of more than 4 elements

        Returns
        -------
        dict
            cluster with length of 4
        """
        number_of_clusters = len(cluster)
        if number_of_clusters > 4:
            rotated_cluster = self.__rotate_Coordinates_to_best_angle(cluster)
            coords = rotated_cluster.values()
            A, C = self.__find_A_and_C(coords)
            vectorA = np.asarray(A)
            vectorC = np.asarray(C)
            distAC = np.linalg.norm(vectorA-vectorC)
            coords.remove(A)
            coords.remove(C)
            for i in range(len(coords)):
                for coord in coords:
                    vector1 = np.asarray(coords[i])
                    vector2 = np.asarray(coord)
                    dist = np.linalg.norm(vector1-vector2)
                    if check_inBetween(dist, distAC*1.1, distAC*0.9):
                        values = [A, C, coords[i], coord]
                        keys = list()
                        for value in values:
                            keys += get_keys_from_value(rotated_cluster, value)
                        to_delete = list(set(cluster.keys()) - set(keys)) + list(set(keys) - set(cluster.keys()))
                        for del_key in to_delete:
                            del cluster[del_key]
                        return cluster
        return cluster
    
    
    def __find_center(self, coords):
        """
        calculating the mean of the x and y value for a list of tuple coordinates

        Parameters
        ----------
        coords : list
            list of tuple like coordinates

        Returns
        -------
        tuple
            (mean x, mean y)
        """
        X = 0
        Y = 0
        n = len(coords)
        for coord in coords:  
            X += coord[0]
            Y += coord[1]
        
        mean_X = round(X/n)
        mean_Y = round(Y/n)
        return (mean_X, mean_Y)
            
            
    def __sort_corners(self):
        """
        find the corners from the "rectangular" shaped grid:
        
        A-------D\n
        |       |\n
        B-------C\n

        Returns
        -------
        dict
            4 corner coordinates
        """
        ###### 0.Step
        # check via the x value which red dot was recognized at first
        # resort the values
        self.__sort_coordiantes()
        ###### 1.Step
        # find corner C and A by summing up the y and y values and using the one with the
        # biggest sum value for C and the lowest for A
        
        coords = list(self.__coordiantes.values())
        A,C = self.__find_A_and_C(coords)
        coords.remove(A)
        coords.remove(C)
        ###### 2.Step
        # determine B and D

        if coords[0][0] < coords[1][0]:
            B = coords[0]
            D = coords[1]
        else:
            D = coords[0]
            B = coords[1]
        return {'A':A,'B':B,'C':C,'D':D}
  
  
    def __sort_coordiantes(self):
        """
        If the image is twisted so that the "wrong" corner is detected
        first, the coordiantes switch back to normal by analysing the
        x value.
        """
        keys = self.__coordiantes.keys()
        p1 = self.__coordiantes[keys[0]]
        p2 = self.__coordiantes[keys[1]]
        p3 = self.__coordiantes[keys[2]]
        p4 = self.__coordiantes[keys[3]]

        if p1[0] < p2[0]:
            self.__coordiantes[keys[0]] = p2
            self.__coordiantes[keys[1]] = p1
        if p3[0] < p4[0]:
            self.__coordiantes[keys[2]] = p4
            self.__coordiantes[keys[3]] = p3
  
  
    def __calculate_missing_knots(self):
        """
        Calculating the missing knots out of the symmetrie
        and the 4 corner coordinates.

        Returns
        -------
        np.array
            3x6 matrix with all coordinates
        """
        # convert the tuple coordinates into numpy arrays
        vectorA = np.asarray(self.corners['A'])
        vectorB = np.asarray(self.corners['B'])
        vectorC = np.asarray(self.corners['C'])
        vectorD = np.asarray(self.corners['D'])
        # creating straight line equations out of the given symmetrie
        upper_h = sle.StraightLineEquation(vectorD, vectorA)
        lower_h = sle.StraightLineEquation(vectorC, vectorB)
        left_v = sle.StraightLineEquation(vectorB, vectorA)
        right_v = sle.StraightLineEquation(vectorC, vectorD)
        middle_h = sle.StraightLineEquation(
            right_v.calculate(1/2), left_v.calculate(1/2))
        # calculating the missing coordinates and putting it into a matrix shape
        # the rows in the matrix are correspond to the horizontal lines in the grid
        coord_Matrix = [[],[],[]]
        for i in range(5, -1, -1):
            x1 = tuple(np.rint(upper_h.calculate(i/5)))
            coord_Matrix[0].append(x1)
            x2 = tuple(np.rint(middle_h.calculate(i/5)))
            coord_Matrix[1].append(x2)
            x3 = tuple(np.rint(lower_h.calculate(i/5)))
            coord_Matrix[2].append(x3)
        
        return coord_Matrix
    
    def __rotate_Coordinates_to_best_angle(self, cluster):
        """
        Rotating the coordinates around the center of the image to
        find the angle where the corners A and C have almost the same
        y-value.

        Parameters
        ----------
        cluster : dict
            clustered coordinates

        Returns
        -------
        dict
            rotated coordinates
        """
        keys = cluster.keys()
        #### 1. step find corner C by looking for the max value of x+y
        Y = cluster[keys[0]][1]
        temp = 0
        corner_C_key = ''
        for key in keys:
            X = cluster[key][0]
            Y = cluster[key][1]
            if (X+Y) > temp:
                temp = X+Y
                corner_C_key = key
                
        reference_X = cluster[corner_C_key][0]
        reference_Y = cluster[corner_C_key][1]
        #### 2. step looking for the point with the shortest y and biggest x shift
        next_key = ''
        minimal_y_shift = 0
        maximal_x_shift = 0
        for key in keys:
            if key != corner_C_key:
                first_check = minimal_y_shift == 0 and maximal_x_shift == 0
                X = cluster[key][0]
                Y = cluster[key][1]
                x_dist = abs(X-reference_X)
                y_dist = abs(Y-reference_Y)
                if x_dist > maximal_x_shift and y_dist < minimal_y_shift or first_check:
                    minimal_y_shift = y_dist
                    maximal_x_shift = x_dist
                    next_key = key
        #### 3. step rotate till y values of corner C and of the point from step 2 are almost equal
        smallest_difference = abs(cluster[next_key][1]-reference_Y)
        best_angle = 0
        stop = 151
        start = -150
        step = 0.1
        ref_angle = 0
        while smallest_difference != 0:
            for angle in np.arange(start, stop, step):
                new_C = self.__rotate(cluster[corner_C_key], angle)
                new_C_Y = new_C[1]
                new_coord = self.__rotate(cluster[next_key], angle)
                new_coord_Y = new_coord[1]
                difference = abs(new_coord_Y - new_C_Y)
                if difference < smallest_difference:
                    smallest_difference = difference
                    best_angle = angle
            if ref_angle != best_angle:
                ref_angle = best_angle
                stop = ref_angle*(1+step)
                start = ref_angle*(1-step)
                step = step/2
            else:
                break   
        rotated_coords =dict()
        for key in keys:
            rotated_coord = self.__rotate(cluster[key], best_angle)
            rotated_coords[key]=rotated_coord
        return rotated_coords
    
    
    def __rotate(self, coord, angle):
        """
        Rotate the 2d coordinates coord at an angle.

        Parameters
        ----------
        coord : tuple
            2d coordinates
        angle : float
            angle in dregrees

        Returns
        -------
        tuple
            new 2d coordinates
        """
        numpy_coord = np.asarray(coord)
        theta = np.radians(angle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s),(s, c)))
        diff = np.subtract(numpy_coord, self.image_center)
        new_coord = self.image_center + R.dot(diff)
        return new_coord[0], new_coord[1]
    
    def __find_A_and_C(self, coords):
        """
        find the coners A and C with the definition, that the sum of x
        and y is by A the smallest and by C the biggest.

        Parameters
        ----------
        coords : list
            list of tuple(x,y) coordinates

        Returns
        -------
        tuple
            coordintes of A and C
        """
        max_sum_val = 0
        min_sum_val = 0
        for coord in coords:
            sum_value = coord[0] + coord[1]
            if sum_value > max_sum_val:
                max_sum_val = sum_value
                min_sum_val = sum_value
                C = coord
            elif sum_value < min_sum_val:
                min_sum_val = sum_value
                A = coord
        return A, C
# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def check_inBetween(value, upper = 0, lower = 0):
    """
    check if the value is in a specified range
    Parameters
    ----------
    value : float
        value to ckeck
    upper : float, optional
        upper limit, by default 0
    lower : float, optional
        lower limit, by default 0
    Returns
    -------
    bool
        is the value in the range
    """
    return lower <= value and value <= upper
 

def round_data(data, err=0, digits=-1):
    """
    round_data
    Round the data by using DIN 1333. The position of the first segnificant␣
    ,→digit of the error
    is used as the the last segnificant digit of the data. If the first␣
    ,→segnificant digit of the error
    is a 1 or 2, one more digit is added.
    Parameters
    ----------
    data : [float]
    floating number with inaccuracy
    err : [float, optional]
    floating number of the data inaccuracy
    Returns
    digits : [int, optional]
    if digits are set, the rounding is not made by DIN 1333
    the numbers will be returned with the wanted number of digits
    -------
    [tuple of str]
    [0] rounded data by DIN 1333
    [1] rounded error by DIN 1333
    """
    if digits >= -1:
        counter = 0
        for number in str(err).replace('.', ''):
            if number == '0':
                counter += 1
            elif number == '1' or number == '2':
                counter += 1
                break
            else:
                break
    else:
        counter = digits
    rounded_err = round(err, counter)
    rounded_data = round(data, counter)
    return rounded_data, rounded_err


def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]

# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    pass



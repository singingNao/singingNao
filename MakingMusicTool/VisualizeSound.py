#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-07-22 13:53:00
# @Author  : Tom Brandherm (s_brandherm19@stud.hwr-berlin.de)
# @Link    : link
# @Version : 1.0.2
# @Python  : 2.7.0
"""
Class for analysing and visualize sounds.
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
import matplotlib.pyplot as plt
import numpy as np
import wave
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class SoundVisualizer(object):

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, raw_data):
        self.raw_data = raw_data

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def plot_soundtracks(self):
        for raw in self.raw_data:
            self.visualize(raw)
    
    
    def visualize(self, raw):
        # reads all the frames
        signal = raw[0]
        # gets the frame rate
        f_rate = raw[1]
        # to Plot the x-axis in seconds
        # you need get the frame rate
        # and divide by size of your signal
        # to create a Time Vector
        # spaced linearly with the size
        # of the audio file
        time = np.linspace(
            0,  # start
            len(signal) / (2*f_rate),
            num=len(signal)
        )
        # using matlplotlib to plot
        # creates a new figure
        plt.figure(1)

        # title of the plot
        plt.title("Sound Wave")

        # label of x-axis
        plt.xlabel("time [s]")
        plt.ylabel("Amplitude")
        # actual ploting
        plt.plot(time, signal, linewidth=0.5)

        # shows the plot
        # in new window
        plt.show()


        # you can also save
        # the plot using
        #plt.savefig(self.path.replace('wav','png'))

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    pass



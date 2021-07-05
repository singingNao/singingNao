#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-05-07 16:05:35
# @Author  : Tom Brandherm (tom.brandherm@msasafety.com)
# @Link    : link
# @Version : 0.0.1
"""
Coming Soon: Making Music with Python
"""
# =========================================================================== #
#  Copyright 2021 MSA Safety as unpublished work
# =========================================================================== #
#  All Rights Reserved.
#  The information contained herein is confidential property of MSA. The use,
#  copying, transfer or disclosure of such information is prohibited except
#  by express written agreement with MSA.
# =========================================================================== #

# =========================================================================== #
#  SECTION: Imports                                                           
# =========================================================================== #
import os

from pydub import AudioSegment
from pydub.playback import play
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class ClassName(object):

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, AttributeName):
        ## public

        ## __private
        self.__AttributeName = AttributeName

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def get_AttributeName(self):
        return self.__AttributeName

    def set_AttributeName(self, AttributeName):
        self.__AttributeName = AttributeName

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def doSomething(self):
        pass

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __doSomethingPrivate(self):
        pass


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    
    
    ###### EXAMPLE ######
    fileName = "Sounds\mixkit-metal-hit-drum-sound-550.wav"
    
    path = os.path.dirname(os.path.abspath(__file__))
    sound_path = os.path.join(path, fileName)
    #input audio file
    sound = AudioSegment.from_file(sound_path, format="wav")
    #cut audio file
    short_sound = sound[:1000] #first two seconds of the audio file (milliseconds) 
    combined = short_sound
    for i in range(5):
        # make the sound i dbB louder
        short_sound = short_sound + i
        # append two sounds
        combined = combined + short_sound 
    
    #play sound
    play(combined)
    
    



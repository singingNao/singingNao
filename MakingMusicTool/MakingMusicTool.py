#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-05-07 16:05:35
# @Author  : Tom Brandherm (tom.brandherm@msasafety.com)
# @Link    : link
# @Version : 0.0.1
"""
Making music with python is possible by using this tool. As a import pattern 
please use a created csv file with one or more rows like:

[one of the given instruments],[volume from 1 to 3],[music note 1],...[music note n]

A 4/4 stroke is used here, so the sum of the notes in one row have to be equals one.
The notation for the notes into the csv is: 

1/16    =>  16
1/8     =>  8
1/4     =>  4
1/2     =>  2
1/1     =>  1
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
import os
import csv

from pydub import AudioSegment
from pydub.playback import play
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
# name of the input csv file
FILENAME = "sound_pattern.csv"
# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class MusicMaker(object):
    """
    MusicMaker is a class to that can create soundtracks out of a given pattern.
    The pattern needs information about a instrument, the volume and a 4/4-stroke
    rythm.
    """
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, fileName: str, bpm:int):
        ## public
        # input from the csv file
        self.sound_pattern = self.analyse_data(fileName)
        ## __private
        # given instrument beat audio files (wav-format!!!)
        self.__instruments =   {'drum': 'mixkit-metal-hit-drum-sound-550.wav',
                                'bass': 'mixkit-bass-guitar-single-note-2331.wav',
                                'tribal drum': 'mixkit-tribal-dry-drum-558.wav'}
        # convert the beats per minutes (bpm) into the duration of one stroke [ms]
        self.__stroke_duration = 60*4/bpm*1000
        # reference volume for the used audio files
        self.__ref_dBFS = -25
        

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def analyse_data(self, fileName:str):
        """
        Import of the csv data and converting it into a dict of sound patterns.

        Parameters
        ----------
        fileName : str
            name of the csv data file

        Returns
        -------
        dict
            sound pattern of the csv file
        """
        # make absolute path
        path = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(path, fileName)
        sound_pattern = dict()
        label = "sound"
        #open csv file
        with open(abs_path, newline='') as file:
            reader = csv.reader(file)
            # iterate through file input
            for i,row in enumerate(reader):
                # delete all empty strings
                row = [x for x in row if x]
                # check if notes are correct defined
                if self.__check_notes(row):
                    # add to dict
                    sound_pattern[label+str(i)]=row
                else:
                    #TODO do something if notes aren't valid
                    print("Check the pattern")
        return sound_pattern
    
    
    def makeMusic(self):
        """
        Use the imported music information to create a soundtrack.
        """
        # silent audio segment with defined length for one stroke
        music = AudioSegment.silent(duration=self.__stroke_duration)
        # iterating though the importet patterns
        for pattern in self.sound_pattern.values():
            # get instrument sound
            sound = self.__choose_instrument(pattern[0])
            # set instrument sound to defined volume
            sound = self.__sync_target_amplitute(sound, self.__ref_dBFS)
            # get the choosen volume
            volume = self.__choose_volume(pattern[1])
            # increase the volume of the audio segment
            sound += volume
            # get the choosen notes
            notes = pattern[2:]
            # create soundtrack of the sound segment and the notes
            soundtrack = self.play_instrument(sound, notes)
            # overlay the new soundtrack to the existing music
            music = music.overlay(soundtrack)
        # squre the music length
        for i in range(2):
            music += music
        #export the new soundtrack file
        music.export('new_music.wav', format='wav')
        #play the new soundtrack via speaker
        play(music)
        
        
    def play_instrument(self, sound: AudioSegment, notes: list):
        """
        Create a soundtrack out of a given instrument sound and a note pattern.

        Parameters
        ----------
        sound : AudioSegment
            instrumental audio segment
        notes : list
            list of notes: 8 => 1/8; 4=>1/4; ...

        Returns
        -------
        AudioSegment
            created soundtrack
        """
        # silent audio segment with defined length for one stroke
        soundtrack = AudioSegment.silent(duration=self.__stroke_duration)
        # first start of the overlay
        time = 0
        # iterating through the list of notes
        for note in notes:
            # overlay of soundtrack and instrumental sound at a defined position
            soundtrack = soundtrack.overlay(sound, position=time)
            # calculating the position of the next overlay out of the notes
            time += self.__stroke_duration/int(note)
        soundtrack = soundtrack.overlay(sound, position=time)
        return soundtrack
    
    
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __check_notes(self, pattern:list):
        """
        check notes if the sum of all notes is equal one

        Parameters
        ----------
        pattern : list
            list of notes

        Returns
        -------
        boolean
            True, if sum is 1
            False, if sum is not equal 1
        """
        four_quarter_sum = 0
        for note in pattern[2:]:
            four_quarter_sum += 1/int(note)
        if four_quarter_sum == 1:
            return True
        return False


    def __choose_instrument(self, instrument:str):
        """
        Choose the instrument out of the user input pattern and returning the
        associated audio segment.

        Parameters
        ----------
        instrument : str
            name of the used instrument

        Returns
        -------
        AudioSegement
            audio segment of the choosen instrument
        """
        for key in self.__instruments:
            if instrument == key:
                fileName = self.__instruments[key]
        path = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(path, 'Sounds',fileName)
        sound = AudioSegment.from_file(abs_path, format="wav")
        return sound
    
    
    def __choose_volume(self, volume:str):
        """
        Converting the input 1,2,3 into the volume change in dB.

        Parameters
        ----------
        volume : str
            input volume 1, 2 or 3

        Returns
        -------
        int
            to increase by volume value
        """
        if volume == '1':
            return 0
        if volume == '2':
            return 2
        if volume == '3':
            return 4

    
    def __sync_target_amplitute(self, sound:AudioSegment, target_dBFS:int):
        """
        Setting the volume of a audio segment to a defined volume.

        Parameters
        ----------
        sound : AudioSegment
            audio segment that should be changed
        target_dBFS : int
            new volume

        Returns
        -------
        AudioSegment
            audio segment with new volume
        """
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)
# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    musicMaker = MusicMaker(FILENAME, bpm=110)
    musicMaker.makeMusic()



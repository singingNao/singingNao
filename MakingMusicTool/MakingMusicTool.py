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
import csv

from pydub import AudioSegment
from pydub.playback import play
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class MusicMaker(object):

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, fileName: str, bpm:int):
        ## public
        self.sound_pattern = self.analyse_data(fileName)
        ## __private
        self.__instruments =   {'drum': 'mixkit-metal-hit-drum-sound-550.wav',
                                'bass': 'mixkit-bass-guitar-single-note-2331.wav', #not working
                                'tribal drum': 'mixkit-tribal-dry-drum-558.wav'}
        self.__stroke_duration = 60*4/bpm*1000 
        self.__ref_dBFS = -20
        

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def analyse_data(self, fileName:str):
        path = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(path, fileName)
        sound_pattern = dict()
        label = "sound"
        with open(abs_path, newline='') as file:
            reader = csv.reader(file)
            for i,row in enumerate(reader):
                row = [x for x in row if x]
                if self.__check_notes(row):
                    sound_pattern[label+str(i)]=row
                else:
                    print("Check the pattern")
        return sound_pattern
    
    def makeMusic(self):
        music = AudioSegment.silent(duration=self.__stroke_duration)
        for pattern in self.sound_pattern.values():
            sound = self.__choose_instrument(pattern[0])
            sound = self.__sync_target_amplitute(sound, self.__ref_dBFS)
            volume = self.__choose_volume(pattern[1])
            sound += volume
            notes = pattern[2:]
            soundtrack = self.play_instrument(sound, notes)
            music = music.overlay(soundtrack)
        for i in range(2):
            music += music
        play(music)
        print(len(music))
        
        
    def play_instrument(self, sound: AudioSegment, notes: list):
        soundtrack = AudioSegment.silent(duration=self.__stroke_duration)
        time = 0
        for note in notes:
            soundtrack = soundtrack.overlay(sound, position=time)
            time += self.__stroke_duration/int(note)
        soundtrack = soundtrack.overlay(sound, position=time)
        return soundtrack
    
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __check_notes(self, pattern:list):
        four_quarter_sum = 0
        for note in pattern[2:]:
            four_quarter_sum += 1/int(note)
        if four_quarter_sum == 1:
            return True
        return False

    def __choose_instrument(self, instrument:str):
        for key in self.__instruments:
            if instrument == key:
                fileName = self.__instruments[key]
        path = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(path, 'Sounds',fileName)
        sound = AudioSegment.from_file(abs_path, format="wav")
        return sound
    
    
    def __choose_volume(self, volume):
        if volume == '1':
            return 0
        if volume == '2':
            return 2
        if volume == '3':
            return 4

    
    def __sync_target_amplitute(self, sound:AudioSegment, target_dBFS:int):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)
# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    fileName = "sound_pattern.csv"
    musicMaker = MusicMaker(fileName, bpm=60)
    musicMaker.makeMusic()



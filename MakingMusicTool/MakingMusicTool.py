#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-05-07 16:05:35
# @Author  : Tom Brandherm (tom.brandherm@msasafety.com)
# @Link    : link
# @Version : 1.0.0
"""
Making music with python is possible by using this tool. As a import pattern 
please use a created csv file with one or more rows like:

[one of the given instruments],[volume from 1 to 3],[music note 1],...[music note n]

A 4/4 time is used here, so the sum of the notes in one row have to be equals one.
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
import matplotlib.pyplot as plt
import numpy as np

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
    The pattern needs information about a instrument, the volume and a 4/4-time
    rhythm.
    """
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, fileName, bpm=60, timeSignature=4):
        ## public
        self.sound_pattern = self.get_sound_pattern_from_csv_file(fileName)
        ## __private
        # given instrument beat audio files (wav-format!!!)
        self.__instruments =   {'drum': 'mixkit-metal-hit-drum-sound-550.wav',
                                'bass': 'mixkit-bass-guitar-single-note-2331.wav',
                                'tribal drum': 'mixkit-tribal-dry-drum-558.wav',
                                'violin': 'mixkit-orchestral-violin-jingle-2280.wav'}
    
        self.__time_signature_duration = self.convert_bpm_to_time_signature_duration_in_ms(bpm, timeSignature)
        # reference volume for the used audio files
        self.__ref_dBFS = -20
        

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def get_sound_pattern_from_csv_file(self, fileName):
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
        absolute_path = get_absolute_path(fileName)
        sound_pattern = dict()
        #open csv file
        with open(absolute_path, 'rb') as file:
            reader = csv.reader(file, delimiter=',')
            # iterate through file input
            for i,row in enumerate(reader):
                # delete all empty strings
                row = [x for x in row if x]
                if self.__are_notes_valid(row[2:]):
                    # add to dict
                    sound_pattern["sound"+str(i)] = row
                else:
                    #TODO do something if notes aren't valid
                    #print(f"Check the pattern of row {i}")
                    print("DS")
        return sound_pattern
    
    
    def create_music_file(self):
        """
        Use the imported music information to create a soundtrack.
        """
        music = AudioSegment.silent(duration=self.__time_signature_duration)
        # iterating though the importet patterns
        for pattern in self.sound_pattern.values():
            sound = self.__get_instrument_sound(pattern[0])
            sound = self.__set_volume(sound, self.__ref_dBFS)
            volume = self.__get_volume_gain(pattern[1])
            sound += volume
            # get the choosen notes
            notes = pattern[2:]
            soundtrack = self.create_soundtrack(sound, notes)
            music = self.__extend_soundtrack(music, soundtrack)
            music = music.overlay(soundtrack)
        music = self.__repeat_soundtrack(count=2, soundtrack=music)
        music.export('new_music.wav', format='wav')
        #print(f'Exported a soundtrack with the lenght of {len(music)}ms')
        # play the new soundtrack via speaker
        # play(music)
        return music
        
        
    def create_soundtrack(self, sound, notes):
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
        soundtrack = AudioSegment.silent(duration=self.__time_signature_duration)
        time = 0
        for note in notes:
            soundtrack = soundtrack.overlay(sound, position=time)
            time += self.__time_signature_duration/int(note)
            soundtrack = self.__extend_soundtrack(soundtrack, sound, time)
        soundtrack = soundtrack.overlay(sound, position=time)
        return soundtrack
    
    
    def delete_silence(self, sound):
        """
        Delete all the silent parts of a soundtrack. 

        Parameters
        ----------
        sound : AudioSegment
            input sound

        Returns
        -------
        AudioSegment
            output sound without silence
        """
        start_trim = self.__detect_leading_silence(sound)
        end_trim = self.__detect_leading_silence(sound.reverse())
        duration = len(sound)
        return sound[start_trim:duration-end_trim]
    
    
    def convert_bpm_to_time_signature_duration_in_ms(self, bpm, timeSignature):
        """
        Convert the bpm value to a duration in ms of timeSignature times beats. 

        Parameters
        ----------
        bpm : int
            beats per minutes
        timeSignature : int
            number of beats per intervall

        Returns
        -------
        float
            duration of one intervall in ms
        """
        return 60*timeSignature/bpm*1000
    
    
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __are_notes_valid(self, notes):
        """
        check notes if the sum of all notes is equal one

        Parameters
        ----------
        pattern : list
            list of notes

        Returns
        -------
        bool
            True, if sum is 1
            False, if sum is not equal 1
        """
        notes_sum = 0
        for note in notes:
            notes_sum += 1/float(note)
        if notes_sum == 1:
            return True
        return False

<<<<<<< HEAD

    def __get_instrument_sound(self, instrument: str) -> AudioSegment:
=======
    def __get_instrument_sound(self, instrument):
>>>>>>> 90a4314c5de1848faf581af3c0aa86de111bc9d2
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
                break
        absolute_path = get_absolute_path("Sounds/" + fileName)
        sound = AudioSegment.from_file(absolute_path, format="wav")
        return self.delete_silence(sound)
        
    
    def __get_volume_gain(self, volume):
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

    
    def __set_volume(self, sound, target_dBFS):
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
    
    
    def __extend_soundtrack(self, main_soundtrack, soundtrack, position=0):
        """
        Checks background sound if a overlay is possible with a front sound. If the fron sound would be cut, 
        the background will be extended.

        Parameters
        ----------
        backgroundSound : AudioSegment
            main soundtrack in the background
        frontSound : AudioSegment
            new sound that should be overlayed over the background
        position : float, optional
            position of the overlay, by default 0

        Returns
        -------
        AudioSegment
            background sound, which is should the situation arises extended
        """
        if (position + len(soundtrack)) > len(main_soundtrack):
            overlap = position + len(soundtrack) - len(main_soundtrack)
            silent = AudioSegment.silent(duration=overlap)
            main_soundtrack += silent
        return main_soundtrack
    
    
    def __detect_leading_silence(self, sound, silence_threshold=-50.0, iteration_size=10):
        """
        iterates over chunks until you find the first one with sound

        Parameters
        ----------
        sound : AudioSegment
            sound in which silence shoulb be detected
        silence_threshold : int, optional
            dB limit for silence, by default -50.0
        chunk_size : int, optional
            chunk of the sound in ms, by default 10

        Returns
        -------
        int
            first time without silence
        """
        trim_position = 0  # ms

        assert iteration_size > 0  # to avoid infinite loop
        while self.__is_silent(iteration_size, silence_threshold, sound, trim_position):
            trim_position += iteration_size
        return trim_position
    
    
    def __is_silent(self, iteration_size, silence_threshold, sound, trim_position):
        """
        checks if the analysed audio segment part is silent (volume below limit) or not. 

        Parameters
        ----------
        iteration_size : int
            size of the audio segment 
        silence_threshold : int
            limit below the audio is defined as silent
        sound : AudioSegment
            whole audio segment object
        trim_position : int
            current position, where the sound is analysed

        Returns
        -------
        bool
            True, if silent
        """
        return sound[trim_position:trim_position + iteration_size].dBFS < silence_threshold and trim_position < len(sound)
    
    
    def __repeat_soundtrack(self, count, soundtrack):
        """
        Repeats and appends the soundtrack 'count' times.

        Parameters
        ----------
        count : int
            number of how many times the soundtrack should be repeated
        soundtrack : AudioSegment
            soundtrack that should be repeated

        Returns
        -------
        AudioSegment
            extended soundtrack
        """
        for i in range(count):
            soundtrack += AudioSegment.silent(duration=self.__time_signature_duration)
            soundtrack = soundtrack.overlay(soundtrack, 
                                            position=self.__time_signature_duration)
        return self.delete_silence(soundtrack)
    
    
# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def get_absolute_path(fileName):
    """
    Returns the absolute path of a file. The file name has to be
    relative to the path of the python script.

    Parameters
    ----------
    fileName : str
        name of the file relative to the script

    Returns
    -------
    str
        absolute path of the file
    """
    path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path, fileName)


def visualize_sound(sound:AudioSegment, title:str="", filters:int=5):
    """
    Visualizes the sound by analysing the frequencies and the spectrum

    Parameters
    ----------
    sound : AudioSegment
        sound to visualize
    title : str, optional
        title of the chart, by default ""
    filters : int, optional
        amound of filters, by default 5
    """
    samples = sound.get_array_of_samples()
    samples = np.array(samples)
    print(samples)
    """spectrum, frequencies = sound.filter_bank(nfilters=filters)
    i = 0
    for freq, (index, row) in zip(frequencies[::-1], enumerate(spectrum[::-1, :])):
        plt.subplot(spectrum.shape[0], 1, index + 1)
        if i == 0:
            plt.title(title)
            i += 1
        plt.ylabel("{0:.0f}".format(freq))
        plt.plot(row)
    plt.show()"""
    
def pydub_to_np(audio: AudioSegment) -> tuple:
    """Converts pydub audio segment into float32 np array of shape [channels, duration_in_seconds*sample_rate],
    where each value is in range [-1.0, 1.0]. Returns tuple (audio_np_array, sample_rate)"""
    # get_array_of_samples returns the data in format:
    # [sample_1_channel_1, sample_1_channel_2, sample_2_channel_1, sample_2_channel_2, ....]
    # where samples are integers of sample_width bytes.
    return np.array(audio.get_array_of_samples(), dtype=np.float32).reshape((-1, audio.channels)).T / (
        1 << (8 * audio.sample_width)), audio.frame_rate


# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #
if __name__ == '__main__':
    musicMaker = MusicMaker(FILENAME, bpm=120)
    music = musicMaker.create_music_file()
    # for debugging
<<<<<<< HEAD
    #visualize_sound(music)
    print('lets see')
    samples = pydub_to_np(music)[0]
    print(samples)
    print(f'{samples[0].shape=}')
    plt.plot(samples[1])
    plt.show()
=======
    #spec, frequencies = music.filter_bank(nfilters=5)
    #visualize_sound(spec, frequencies)
>>>>>>> 90a4314c5de1848faf581af3c0aa86de111bc9d2



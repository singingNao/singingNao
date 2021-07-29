#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-07-29 23:05:35
# @Author  : Omar El-Haj-Mohamad (omar.el-haj@web.de)
# @Link    : link
# @Version : 1.0.0
"""
This module build a connection to your Nao and react to existing and created events.
The module use the MusicMakerTool to create a music file from recognized objects.
Please edit PIP with the IP-Address of your nao.
You have to run it before starting the program in Choreograph.
To run this module make sure that you are using python 2.7 and on your system is the naoqi framework installed.
"""

import qi
import sys
import time
from MakingMusicTool.MakingMusicTool import MusicMaker

PIP = "192.168.38.118"
PPORT = 9559

class PictureDetactionModule(object):
    """
    Module to react on Event PictureDetected, AllDetectFromFileEventsTriggered and CreateMusicFile
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        :param app: Application to build a connection to Nao
        """
        # Constructor of super klass
        super(PictureDetactionModule, self).__init__()
        # Start connection to Nao
        app.start()
        self.session = app.session

        # Get the service ALMemory.
        self.memory = self.session.service("ALMemory")
        # Get the service ALTextToSpeeach.
        self.tts = self.session.service("ALTextToSpeech")
        # Get the service ALVisionRecognition.
        self.vision_recognition = self.session.service("ALVisionRecognition")
        self.vision_recognition.subscribe("VisionRecognition", 500, 0.0)

        # Connect the event callback PictureDetected.
        # The Event PictureDetected is a standard event of ALMemory.
        # Callback function is on_picture_detected
        self.picture_detected_subscriber = self.memory.subscriber("PictureDetected")
        self.picture_detected_subscriber.signal.connect(self.on_picture_detected)

        # Create new event "AllDetectFromFileEventsTriggered"
        # Connect the event callback AllDetectFromFileEventsTriggered
        # Callback function is on_all_detect_from_file_events_triggered
        self.memory.declareEvent("AllDetectFromFileEventsTriggered")
        self.all_detect_from_file_events_triggered_subscriber = self.memory.subscriber("AllDetectFromFileEventsTriggered")
        self.all_detect_from_file_events_triggered_subscriber.signal.connect(self.on_all_detect_from_file_events_triggered)

        # Create new event "CreateMusicFile"
        # Connect the event callback CreateMusicFile
        # Callback function is on_create_music_file
        self.memory.declareEvent("CreateMusicFile")
        self.create_music_file_subscriber = self.memory.subscriber("CreateMusicFile")
        self.create_music_file_subscriber.signal.connect(self.on_create_music_file)

        self.music_maker = MusicMaker()
        self.music_beats_counter = 0 # needed to create more than one beat before creating music file
        self.note_index = 1 # needed to write in the correct note index of an beat

        self.got_picture = False

    def on_picture_detected(self, value):
        """
        Callback for event PictureDetected.
        If picture is detected, it will be stored in music_beats

        Parameters
        ----------
        value: [ TimeStamp, PictureInfo[N] ]
               http://doc.aldebaran.com/2-8/naoqi/vision/alvisionrecognition.html

        """
        if value == []:
            self.got_picture = False
        elif not self.got_picture:
            try:
                self.got_picture = True
                music_card_category = value[1][0][0][0]
                music_card_name = value[1][0][0][1]
                if music_card_category == "instrument":
                    self.music_maker.set_music_beats(self.music_beats_counter, "instrument", music_card_name)
                elif music_card_category == "volume":
                    self.music_maker.set_music_beats(self.music_beats_counter, "volume", music_card_name)
                elif music_card_category == "note":
                    if self.note_index > 8:
                        self.tts.say("Can not add " + music_card_name)
                    else:
                        self.music_maker.set_music_beats(self.music_beats_counter, "note" + str(self.note_index), music_card_name)
                        self.note_index += 1
            except Exception, e:
                print(e)


    def on_all_detect_from_file_events_triggered(self, value):
        """
        Callback for event AllDetectFromFileEventsTriggered.

        Parameters
        ----------
        value: second Parameter from function raising the event

        """
        self.tts.say(str(value))
        self.music_maker.add_ordered_dict_to_music_beats()
        self.music_beats_counter += 1
        self.note_index = 1
        print(self.music_maker.music_beats)


    def on_create_music_file(self, value):
        """
        Callback for event AllDetectFromFileEventsTriggered.

        Parameters
        ----------
        value: second Parameter from function raising the event

        """
        self.music_maker.create_music_file()
        self.music_beats_counter = 0
        self.music_maker.music_beats = []
        self.music_maker.add_ordered_dict_to_music_beats()
        self.tts.say(str(value))
        print(value)

        #TODO send file via scp

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting Event callbacks"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping VisionRecognition"
            self.vision_recognition.unsubscribe("VisionRecognition")
            # stop
            sys.exit(0)

if __name__ == '__main__':
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + PIP + ":" + str(PPORT)
        app = qi.Application(["PictureDetactionModule", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi")
        sys.exit(1)
    picture_detector = PictureDetactionModule(app)
    picture_detector.run()
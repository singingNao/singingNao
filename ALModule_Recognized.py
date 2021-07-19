import qi
import sys
import time

PIP = "192.168.226.118"
PPORT = 9559
PATH = "/data/home/nao/project21/singingNao2.7/MakingMusicTool/"

class PictureDetactionModule(object):
    """
    Module to react on Event PictureDetected
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        :param app: Application to build a connection to Nao
        """
        super(PictureDetactionModule, self).__init__()
        app.start()
        self.session = app.session

        # Get the service ALMemory.
        self.memory = self.session.service("ALMemory")

        # Connect the event callback.
        self.subscriber = self.memory.subscriber("PictureDetected")
        self.subscriber.signal.connect(self.on_picture_detected)

        # Get the services ALTextToSpeech and ALVisionRecognition.
        self.tts = self.session.service("ALTextToSpeech")
        self.vision_recognition = self.session.service("ALVisionRecognition")
        self.vision_recognition.subscribe("VisionRecognition", 500, 0.0)
        self.got_picture = False
        self.note_index = 1
        self.music_dict = dict()

    def on_picture_detected(self, value):
        """
        Callback for event PictureDetected.
        """

        if value == []:  # empty value when the recognized object disappears
            self.got_picture = False
        elif not self.got_picture:  # only speak the first time a recognized object appears
            self.got_picture = True
            # self.tts.say("I saw a recognized object! ")
            # First Field = TimeStamp.
            timeStamp = value[0]
            # print "TimeStamp is: " + str(timeStamp)
            music_card_category = value[1][0][0][0]
            music_card_name = value[1][0][0][1]

            if music_card_category == "instrument":
                self.note_index = 1
                self.music_dict = dict()
                self.music_dict["instrument"]= music_card_name
            elif music_card_category == "volume":
                self.music_dict["volume"]= music_card_name
            elif music_card_category == "note":
                self.music_dict["note" + str(self.note_index)] = music_card_name
                self.note_index += 1
            self.tts.say(music_card_name)


        print self.music_dict



    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting VisionRecognition"
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
        #connection_url = "tcp://" + args.ip + ":" + str(args.port)
        connection_url = "tcp://" + PIP + ":" + str(PPORT)
        app = qi.Application(["PictureDetactionModule", "--qi-url=" + connection_url])
    except RuntimeError:
        #print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
         #      "Please check your script arguments. Run with -h option for help.")
        print ("Can't connect to Naoqi")
        sys.exit(1)
    picture_detector = PictureDetactionModule(app)
    picture_detector.run()
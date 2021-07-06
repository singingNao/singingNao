from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBroker

IP = "127.0.0.1"
PORT = 9559
# def startProcess():
#
#     # Speak
#     ttsProxy = ALProxy("ALTextToSpeech", IP, PORT)
#     ttsProxy.say("Hello let us play a game")
#
#     # take a picture
#     global photoCaptureProxy
#     try:
#         photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
#     except Exception as e:
#         print("Error when creating ALPhotoCapture proxy:")
#         print(str(e))
#         exit(1)
#
#     photoCaptureProxy.setResolutions(3)
#     photoCaptureProxy.setPictureFormat("jpg")
#     photoCaptureProxy.takePicture("/home/nao/recordings/cameras/", "gameBoard")
#


class CropperToolModule(ALModule):
    """ A Module to cropp the game boad and seperate it to cards"""

    def __init__(self, name):
        ALModule.__init__(self, name)
        self.name = name


    def exit(self):


    def croppImage(filename):
        """ Cropp the image"""
        tool = CropperTool.CropoerTool()
        tool.seperate_the_objects(filename)


if __name__ == '__main__':

    myBroker = ALBroker("myBroker", "0.0.0.0", IP, PORT)
    global CropperTool
    CropperTool = CropperToolModule("CropperTool")

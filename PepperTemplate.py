#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

""" PepperTemplate """
from __future__ import print_function
import qi
import time
import sys
import argparse
from naoqi import ALProxy
import threading
from random import randint


class PepperTemplate(object):

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(PepperTemplate, self).__init__()
        app.start()
        session = app.session
        # Get the services
        self.memory = session.service("ALMemory")
        self.tts = session.service("ALTextToSpeech")
        self.animation = session.service("ALAnimationPlayer")
        self.ALDialog = session.service("ALDialog")
        self.animatedSay = session.service("ALAnimatedSpeech")

        self.ALFaceDetectionProxy = session.service("ALFaceDetection")

        self.postureProxy = session.service("ALRobotPosture")
        self.behavior = session.service("ALBehaviorManager")

        # Subscriber
        self.p_doAction_subscriber = self.memory.subscriber("P_DOACTION")
        self.p_doAction_subscriber_signal = self.p_doAction_subscriber.signal.connect(self.p_doAction)

        self.p_headTouched_subscriber = self.memory.subscriber("FrontTactilTouched")
        self.p_headTouched_subscriber_signal = self.p_headTouched_subscriber.signal.connect(self.p_headTouched)

        self.p_faceDetected_subscriber = self.memory.subscriber("FaceDetected")
        self.p_faceDetected_subscriber_signal = self.p_faceDetected_subscriber.signal.connect(self.p_faceDetected)

        self.p_getSavedFaces_subscriber = self.memory.subscriber("P_GETSAVEDFACES")
        self.p_getSavedFaces_subscriber_signal = self.p_getSavedFaces_subscriber.signal.connect(self.p_getSavedFaces)

        self.enableRecognition = False

        self.p_toggleFaceDetection_subscriber = self.memory.subscriber("ToggleFaceDetection")
        self.p_toggleFaceDetection_subscriber_signal = self.p_toggleFaceDetection_subscriber.signal.connect(self.p_toggleFaceDetection)

        self.postureProxy.goToPosture('StandInit', 0.5)

        # Get the service tablet
        self.tablet = session.service('ALTabletService')
        self.tablet.resetTablet()
        self.tablet.setBrightness(1)

        # BasicAwareness
        self.life = session.service("ALAutonomousLife")
        self.life.setAutonomousAbilityEnabled("BasicAwareness", True)
        self.life.setAutonomousAbilityEnabled("AutonomousBlinking", True)

        self.motionProxy = session.service("ALMotion")
        # self.audioProxy = ALProxy("ALAudioPlayer", '127.0.0.1', 9559)
        # self.animation_player_service = ALProxy("ALAnimationPlayer", '127.0.0.1', 9559)
        self.motionProxy.wakeUp()
        self.ALDialog.setLanguage("English")

        # Volume/Pitch/Speed
        self.tts.setVolume(1)
        self.tts.setParameter("speed", 0.7)
        self.tts.setParameter("pitchShift", 1.2)


    def p_doAction(self, event):
        self.p_doAction_subscriber.signal.disconnect(self.p_doAction_subscriber_signal)

        if self.ALFaceDetectionProxy.learnFace(event):
            self.animatedSay.say("Face Learned!")
        else:
            self.animatedSay.say("Learning failed!")


        self.p_doAction_subscriber_signal = self.p_doAction_subscriber.signal.connect(self.p_doAction)

    def p_getSavedFaces(self, event):
        self.p_getSavedFaces_subscriber.signal.disconnect(self.p_getSavedFaces_subscriber_signal)

        self.animatedSay.say("Get Saved faces")
        val = self.ALFaceDetectionProxy.getLearnedFacesList()
        print(val);

        self.p_getSavedFaces_subscriber_signal = self.p_getSavedFaces_subscriber.signal.connect(self.p_getSavedFaces)


    def p_faceDetected(self, event):
        if self.enableRecognition is False:
            return

        self.p_faceDetected_subscriber.signal.disconnect(self.p_faceDetected_subscriber_signal)

        if len(event) >= 2:
            if len(event[1]) >= 2:
                if len(event[1][0]) >= 2:
                    if(len(event[1][0][1]) >= 3):
                        name = event[1][0][1][2]
                        print(name)
                        self.animatedSay.say("Hi " + name + " !")


        self.p_faceDetected_subscriber_signal = self.p_faceDetected_subscriber.signal.connect(self.p_faceDetected)

    def p_toggleFaceDetection(self, event):
        print(self.enableRecognition)
        self.enableRecognition = not self.enableRecognition

    def p_headTouched(self, event):
        self.p_headTouched_subscriber.signal.disconnect(self.p_headTouched_subscriber_signal)

        self.animatedSay.say("Auwh! Why did you touch my head?")

        self.p_headTouched_subscriber_signal = self.p_headTouched_subscriber.signal.connect(self.p_headTouched)

    def t_doAction(self):
        self.memory.raiseEvent("T_RECEIVEACTION", 'parameter')

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print ("Starting Pepper Template !")

        self.tablet.cleanWebview()
        self.tablet.loadApplication("PepperTemplate")
        self.tablet.showWebview()
        print(self.ALFaceDetectionProxy.isRecognitionEnabled())
        print(self.ALFaceDetectionProxy.isTrackingEnabled())
        print("recognition treshold")
        print(self.ALFaceDetectionProxy.getRecognitionConfidenceThreshold())
        self.ALFaceDetectionProxy.setRecognitionConfidenceThreshold(0.4)

        #self.ALFaceDetectionProxy.clearDatabase()
        #self.p_getSavedFaces()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print ("Interrupted by user, stopping PepperTemplate")
            self.tablet.hideWebview()
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["PepperTemplate", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    PepperTemplate = PepperTemplate(app)
    PepperTemplate.run()

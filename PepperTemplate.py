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
        self.animatedSay = ALProxy("ALAnimatedSpeech","127.0.0.1",9559)
        self.postureProxy = ALProxy("ALRobotPosture", '127.0.0.1', 9559)
        #self.animatedSay = session.service("ALAnimatedSpeechProxy")
        self.behavior = session.service("ALBehaviorManager")

        # Subscriber
        self.p_doAction_subscriber = self.memory.subscriber("P_DOACTION")
        self.p_doAction_subscriber_signal = self.p_doAction_subscriber.signal.connect(self.p_doAction)

        self.p_headTouched_subscriber = self.memory.subscriber("FrontTactilTouched")
        self.p_headTouched_subscriber_signal = self.p_headTouched_subscriber.signal.connect(self.p_headTouched)

        self.postureProxy.goToPosture('StandInit', 0.5)

        # The picture object
        # Get the service tablet
        self.tablet = session.service('ALTabletService')
        self.tablet.resetTablet()
        self.tablet.setBrightness(1)
        self.session = session

        # BasicAwareness
        # stop the moving
        self.life = session.service("ALAutonomousLife")
        self.life.setAutonomousAbilityEnabled("BasicAwareness", False)
        self.life.setAutonomousAbilityEnabled("AutonomousBlinking", True)
        self.motionProxy  = ALProxy("ALMotion", '127.0.0.1', 9559)
        self.audioProxy = ALProxy("ALAudioPlayer", '127.0.0.1', 9559)
        self.animation_player_service = ALProxy("ALAnimationPlayer",'127.0.0.1', 9559)
        self.motionProxy.wakeUp()
        self.ALDialog.setLanguage("English")

        # Volume/Pitch/Speed
        self.tts.setVolume(1)
        self.tts.setParameter("speed", 0.7)
        self.tts.setParameter("pitchShift", 1.2)

        # # All Leds of Pepper
        # self.leds = ALProxy("ALLeds","127.0.0.1",9559)
        # EyeLeds = ["RightFaceLed1","RightFaceLed2","RightFaceLed3","RightFaceLed4","RightFaceLed5","RightFaceLed6","RightFaceLed7","RightFaceLed8",
        #         "LeftFaceLed1","LeftFaceLed2","LeftFaceLed3","LeftFaceLed4","LeftFaceLed5","LeftFaceLed6","LeftFaceLed7","LeftFaceLed8"]
        # EarLeds = ["LeftEarLeds", "RightEarLeds"]
        # self.leds.createGroup("eyeLeds",EyeLeds)
        # self.leds.createGroup("earLeds",EarLeds)
        # self.leds.off("eyeLeds")
        # self.leds.off("earLeds")
        # self.leds.setIntensity("eyeLeds", 0)
        # self.leds.setIntensity("earLeds", 0)
        # self.leds.fadeRGB("eyeLeds", "green", 1)
        # self.leds.fadeRGB("eyeLeds", "yellow", 1)

        self.motions = [
            "animations/Stand/Emotions/Positive/Hysterical_1",
            "animations/Stand/Gestures/Enthusiastic_4",
            "animations/Stand/Gestures/Enthusiastic_5",
            "animations/Stand/Gestures/Excited_1",
            "animations/Stand/Gestures/No_1",
            "animations/Stand/Gestures/No_2",
            "animations/Stand/Gestures/No_3",
            "animations/Stand/Gestures/No_8",
            "animations/Stand/Gestures/No_9",
            "animations/Stand/Gestures/Nothing_2",
            "animations/Stand/Gestures/ShowSky_1",
            "animations/Stand/Gestures/ShowSky_11",
            "animations/Stand/Gestures/ShowSky_2",
            "animations/Stand/Gestures/ShowSky_4",
            "animations/Stand/Gestures/ShowSky_5",
            "animations/Stand/Gestures/ShowSky_6",
            "animations/Stand/Gestures/ShowSky_7",
            "animations/Stand/Gestures/ShowSky_8",
            "animations/Stand/Gestures/ShowSky_9",
            "animations/Stand/Gestures/Yes_1",
            "animations/Stand/Gestures/Yes_2",
            "animations/Stand/Gestures/Yes_3",
            "animations/Stand/Gestures/YouKnowWhat_1",
            "animations/Stand/Gestures/YouKnowWhat_2",
            "animations/Stand/Gestures/YouKnowWhat_3",
            "animations/Stand/Gestures/YouKnowWhat_5",
            "animations/Stand/Gestures/YouKnowWhat_6",
            "animations/Stand/Gestures/You_1",
            "animations/Stand/Gestures/You_4",
            "animations/Stand/Waiting/ShowSky_1",
            "animations/Stand/Waiting/ShowSky_2",
        ]

    def p_doAction(self, event):
        self.p_doAction_subscriber.signal.disconnect(self.p_doAction_subscriber_signal)

        print("Do action")

        self.animatedSay.say(event)

        self.p_doAction_subscriber_signal = self.p_doAction_subscriber.signal.connect(self.p_doAction)

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
        self.t_doAction()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print ("Interrupted by user, stopping PepperTemplate")
            self.tablet.hideWebview()

            #self.confirmPictureSubscriber.signal.disconnect(self.confirmPictureSubscriberSignal)
            #self.headTouchedSubscriber.signal.disconnect(self.headTouchedSubscriberSignal)
            #self.TakePictureSubscriber.signal.disconnect(self.TakePictureSubscriberSignal)
            # stop
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
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    PepperTemplate = PepperTemplate(app)
    PepperTemplate.run()

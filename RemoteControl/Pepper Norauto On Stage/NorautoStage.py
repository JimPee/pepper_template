#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

""" NorautoStage """
from __future__ import print_function
import qi
import time
import sys
import argparse
from naoqi import ALProxy

class NorautoStage(object):
    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """

        super(NorautoStage, self).__init__()
        app.start()
        session = app.session
        # Get the services
        self.memory = session.service("ALMemory")
        self.tts = session.service("ALTextToSpeech")
        self.animation = session.service("ALAnimationPlayer")
        self.animatedSay = ALProxy("ALAnimatedSpeech","127.0.0.1",9559)
        #self.animatedSay = session.service("ALAnimatedSpeechProxy")
        self.behavior = session.service("ALBehaviorManager")

        # Connect the event callback.
        self.p_emotion_subscriber = self.memory.subscriber("P_EMOTION")
        self.p_emotion_subscriber_signal = self.p_emotion_subscriber.signal.connect(self.p_emotion)

        self.p_wakeup_subscriber = self.memory.subscriber("P_WAKEUP")
        self.p_wakeup_subscriber_signal = self.p_wakeup_subscriber.signal.connect(self.p_wakeup)

        self.headTouchedSubscriber = self.memory.subscriber("FrontTactilTouched")
        self.headTouchedSubscriberSignal = self.headTouchedSubscriber.signal.connect(self.on_head_touched)

        # The picture object
        # Get the service tablet
        self.tablet = session.service('ALTabletService')
        self.tablet.resetTablet()
        #self.tablet.goToSleep()
        self.tablet.setBrightness(0)

        self.wakeUpEnabled = True
        self.session = session

        # BasicAwareness
        # stop the moving
        self.life = session.service("ALAutonomousLife")
        self.life.setAutonomousAbilityEnabled("BasicAwareness", False)
        self.life.setAutonomousAbilityEnabled("AutonomousBlinking", False)
        self.motionProxy  = ALProxy("ALMotion", '127.0.0.1', 9559)

        self.animation.reset()

        if self.wakeUpEnabled:
            self.motionProxy.rest()
        else:
            self.motionProxy.wakeUp()

        # Volume/Pitch/Speed
        self.tts.setVolume(1)
        self.tts.setParameter("speed", 0.2)
        self.tts.setParameter("pitchShift", 1.2)

        # Sentences to say
        self.sentence1 = "Hello, I am Pepper! I am honorred to introduce the presentation of today! Please welcome Patrick"
        self.sentence2 = "Hello Patrick"

        self.headTouchedFlag = True

        # All Leds of Pepper
        self.leds = ALProxy("ALLeds","127.0.0.1",9559)

        #self.blinking = session.service("AutonomousBlinkingProxy")

        #self.blinkOptions = ALProxy("AutonomousBlinking","127.0.0.1",9559)
        # self.blinkOptions.setEnabled(False)
        EyeLeds = ["RightFaceLed1","RightFaceLed2","RightFaceLed3","RightFaceLed4","RightFaceLed5","RightFaceLed6","RightFaceLed7","RightFaceLed8",
                "LeftFaceLed1","LeftFaceLed2","LeftFaceLed3","LeftFaceLed4","LeftFaceLed5","LeftFaceLed6","LeftFaceLed7","LeftFaceLed8"]
        EarLeds = ["LeftEarLeds", "RightEarLeds"]
        self.leds.createGroup("eyeLeds",EyeLeds)
        self.leds.createGroup("earLeds",EarLeds)
        self.leds.off("eyeLeds")
        self.leds.off("earLeds")
        #self.leds.createGroup("earLeds", EarLeds)
        self.leds.setIntensity("eyeLeds", 0)
        self.leds.setIntensity("earLeds", 0)
        #self.leds.fadeRGB("eyeLeds", "green", 1)
        #self.leds.fadeRGB("eyeLeds", "yellow", 1)

    def p_wakeup(self, event):
        if self.wakeUpEnabled:
            #self.tablet.wakeUp()
            self.tablet.setBrightness(1)
            self.leds.setIntensity("eyeLeds", 1)
            self.leds.setIntensity("earLeds", 1)

            #self.tablet.setBrightness(1)
            self.motionProxy.wakeUp()
            self.life.setAutonomousAbilityEnabled("BasicAwareness", True)
            self.life.setAutonomousAbilityEnabled("AutonomousBlinking", True)
            configuration = {"bodyLanguageMode":"contextual"}
            # self.animation.run("animations/Stand/Gestures/Hey_1", _async=True)
            # self.animatedSay.say(self.sentence1, configuration)

            motion = "animations/Stand/Gestures/Hey_4"
            future = self.animation.run(motion, _async=True)
            self.tts.say(
                "Hello \\emph=1\\everyone, thank you for being \\emph=1\\here today. \\pau=500\\ I'm \\emph=1\\Pepper.")
            future.value()

            motion = "animations/Stand/Gestures/Excited_1"
            future = self.animation.run(motion, _async=True)
            self.tts.say(
                "\\pau=500\\ I'm here to introduce the presentation for the 5-years  \\emph=2\\  strategic plan  and the 10-years \\emph=2\\  vision for  \\emph=1\\  Norauto.")
            future.value()

            motion = "animations/Stand/Gestures/Everything_4"
            future = self.animation.run(motion, _async=True)
            self.tts.say("\\pau=500\\ We will discover \\emph=2\\ together \\pau=500\\ what the \\emph=2\\future awaits us.")
            future.value()

            motion = "animations/Stand/Gestures/Everything_3"
            future = self.animation.run(motion, _async=True)
            self.tts.say("\\pau=500\\ I hope to be \\emph=2\\part of it.")
            future.value()

            motion = "animations/Stand/Gestures/Explain_1"
            future = self.animation.run(motion, _async=True)
            self.tts.say(
                "\\pau=500\\ I hand over to \\emph=1\\ Marion, \\emph=1\\ Matthew \\pau=500\\ and \\emph=1\\Patrick \\emph=1\\  \\pau=500\\ who will lead the meeting this afternoon.")
            future.value()

            motion = "animations/Stand/Gestures/Explain_1"
            future = self.animation.run(motion, _async=True)
            self.tts.say("\\pau=500\\ We'll meet again at the cocktail.")
            future.value()

            motion = "animations/Stand/Gestures/ShowSky_4"
            future = self.animation.run(motion, _async=True)
            self.tts.say("\\pau=500\\ Have a \\emph=2\\ good time \\pau=500\\ and See you later.")
            future.value()

            self.animation.run("animations/Stand/Emotions/Positive/Winner_2", _async=True)


            # Pepper calls Patrick on the stage with clapped animation

    def p_emotion(self, event):
        self.p_emotion_subscriber.signal.disconnect(self.p_emotion_subscriber_signal)

        print('Emotion animation : ' + event)

        animations = {
        	"happy": "animations/Stand/Emotions/Positive/Amused_1",
            "affirmative": "animations/Stand/Emotions/Positive/Enthusiastic_1",
            "yesNod": "animations/Stand/Emotions/Positive/Sure_1",
            "explain":  "animations/Stand/Gestures/Explain_4",
            "thinking": "animations/Stand/Waiting/ScratchHead_1",
            "applause": "animations/Stand/Emotions/Positive/Excited_2",
            "suprised": "animations/Stand/Emotions/Negative/Surprise_2",
            "handright": "animations/Stand/Gestures/Far_3",
            "handleft": "animations/Stand/Gestures/Far_1",
            "call": "animations/Stand/Waiting/CallSomeone_1",
            "drink": "animations/Stand/Waiting/Drink_1",
            "guitar": "animations/Stand/Waiting/AirGuitar_1",
        }

        animationToRun = animations[event]
        self.animation.run(animationToRun, _async=True)
        if (event == "drink"):
            self.leds.rasta(5)

        self.p_emotion_subscriber_signal = self.p_emotion_subscriber.signal.connect(self.p_emotion)
        print('Emotion ended')

    def on_head_touched(self, event):

        self.headTouchedSubscriber.signal.disconnect(self.headTouchedSubscriberSignal)

        print("head touched")
        self.animatedSay.say(self.sentence1, configuration)

        self.headTouchedSubscriberSignal = self.headTouchedSubscriber.signal.connect(self.on_head_touched)
        # print (self.headTouchedFlag)
        # if self.headTouchedFlag:
        #     self.headTouchedFlag = False
        #     # Unsubscribe to the event to avoid multiple event firing
        #     self.headTouchedSubscriber.signal.disconnect(self.headTouchedSubscriberSignal)
        #     print('Head is Touched')
        #
        #     future = self.animation.run("animations/Stand/Gestures/Explain_5", _async=True)
        #     self.tts.say("Prepare for the picture")
        #
        #     # future = self.animation.run("animations/Stand/Waiting/TakePicture_1", _async=True)
        #     # future.value()
        #
        #     # Call the front-end
        #     print('Raise event : HeadTouched')
        #     self.memory.raiseEvent("HeadTouched", 1)
        #     future.value()

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print ("Starting Pepper Norauto on Stage !")

        self.tablet.cleanWebview()
        self.tablet.loadApplication("NorautoLogo")
        self.tablet.showWebview()
        #self.tablet.turnScreenOn(False)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print ("Interrupted by user, stopping NorautoStage")
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
        app = qi.Application(["NorautoStage", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    NorautoStage = NorautoStage(app)
    NorautoStage.run()

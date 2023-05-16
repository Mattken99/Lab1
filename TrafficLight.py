from Displays import *
from Button import *
from Buzzer import *
from CompositeLights import *
import time

# TrafficLight class for controlling the individual lights
class TrafficLight:
    def __init__(self, green_pin, yellow_pin, red_pin):
        print("TrafficLight constructor: add the lights in order")
        self._green = Pin(green_pin, Pin.OUT)
        self._yellow = Pin(yellow_pin, Pin.OUT)
        self._red = Pin(red_pin, Pin.OUT)

    def go(self):
        # Turn on green light, turn off others
        print("GO")
        self._green.on()
        self._yellow.off()
        self._red.off()

    def caution(self):
        # Turn on yellow light, turn off others
        print("CAUTION")
        self._green.off()
        self._yellow.on()
        self._red.off()

    def stop(self):
        # Turn on red light, turn off others
        print("STOP")
        self._green.off()
        self._yellow.off()
        self._red.on()

    def run(self):
        # Run the default traffic light pattern: green, yellow, red
        print("Trafficlight - run pattern")
        self.go()
        sleep(5)
        self.caution()
        sleep(3)
        self.stop()
        sleep(5)

# Cycle class for managing the traffic light cycle and button events
class Cycle:
    def __init__(self):
        print("Cycle: Constructor")
        self._traffic = TrafficLight(16, 18, 19)  # Initialize TrafficLight instance
        self._display = LCDDisplay(sda=0, scl=1, i2cid=0)  # Initialize LCD Display instance
        self._button = Button(4, "Request Crossing", buttonhandler=self, lowActive=True)  # Initialize Button instance
        self._buzzer = PassiveBuzzer(13)  # Initialize PassiveBuzzer instance
        self._buttonPressed = False  # Flag to track button state

    def reset(self):
        # Reset the display
        print("Cycle: reset")
        self._display.reset()

    def buttonPressed(self, name):
        # Button press event handler
        print("Button Pressed")
        self._buttonPressed = True
        self._buzzer.beep(300, 1000)  # Emit a beep sound

    def buttonReleased(self, name):
        # Button release event handler
        pass

    def lightcycle(self):
        original_pattern = True  # Track the original traffic pattern
        remaining_time = 0  # Track remaining time for "Walk"
        while True:
            if self._buttonPressed:
                print("Pedestrian Pattern")
                self._display.showText("Walk")
                self._traffic.stop()
                remaining_time = 9  # Set initial remaining time
                while remaining_time > 0:
                    self._display.showText("Walk " + str(remaining_time))  # Display "Walk" with remaining time
                    sleep(1)
                    remaining_time -= 1
                self.reset()
                original_pattern = False
                self._buttonPressed = False
            else:
                if original_pattern:
                    print("Original Pattern")
                    self._display.showText("Don't Walk")
                    self._traffic.go()
                    sleep(5)
                    self._traffic.caution()
                    sleep(3)
                    self._traffic.stop()
                    sleep(5)
                    self.reset()
                else:
                    self._display.showText("Don't Walk")
                    self._traffic.run()
                    self.reset()
                    original_pattern = True

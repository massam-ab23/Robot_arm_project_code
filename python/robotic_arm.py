from time import sleep
from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
from oled import Write
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
import framebuf

# I2C / OLED setup
I2C_ID = 1
SDA_PIN = 14
SCL_PIN = 15
I2C_FREQ = 400000
OLED_WIDTH = 128
OLED_HEIGHT = 64

# Button pins
BUTTON_1_PIN = 10
BUTTON_2_PIN = 11
BUTTON_3_PIN = 20
BUTTON_4_PIN = 21
BUTTON_5_PIN = 28

# Servo pins
SERVO_1_PIN = 2
SERVO_2_PIN = 3
SERVO_3_PIN = 4
SERVO_4_PIN = 5
SERVO_FREQ = 50

# Servo limits / initial positions
DEGREE_MIN = 0
DEGREE_MAX = 180
SERVO_4_MIN = 10
SERVO_4_MAX = 150

deg1 = 100
deg2 = 170
deg3 = 0
deg4 = 145
gripper_direction = 0

i2c = I2C(I2C_ID, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=I2C_FREQ)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

button1 = Pin(BUTTON_1_PIN, Pin.IN, Pin.PULL_UP)
button2 = Pin(BUTTON_2_PIN, Pin.IN, Pin.PULL_UP)
button3 = Pin(BUTTON_3_PIN, Pin.IN, Pin.PULL_UP)
button4 = Pin(BUTTON_4_PIN, Pin.IN, Pin.PULL_UP)
button5 = Pin(BUTTON_5_PIN, Pin.IN, Pin.PULL_UP)

servo1 = PWM(Pin(SERVO_1_PIN))
servo2 = PWM(Pin(SERVO_2_PIN))
servo3 = PWM(Pin(SERVO_3_PIN))
servo4 = PWM(Pin(SERVO_4_PIN))

for servo in (servo1, servo2, servo3, servo4):
    servo.freq(SERVO_FREQ)

write15 = Write(oled, ubuntu_mono_15)
write20 = Write(oled, ubuntu_mono_20)

buffer = bytearray(
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
)


def show_startup_screen():
    write20.text("Robot Arm", 10, 15)
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
    oled.blit(fb, 77, 10)
    oled.show()
    sleep(3)
    oled.fill(0)


def set_servo_cycle(servo, position):
    duty = position * 45 + 1000
    servo.duty_u16(duty)

"""
Robot Arm Control System using MicroPython

Description:
This script controls a multi-servo robotic arm using a microcontroller (e.g., Raspberry Pi Pico).
It integrates button inputs, PWM-based servo control, and an OLED display for real-time feedback.

Features:
- Controls 4 servo motors using PWM signals
- Uses 5 push buttons to adjust servo positions interactively
- Displays current servo angles on an SSD1306 OLED screen
- Supports bidirectional control of the gripper (servo 4)
- Includes a startup screen with graphics

Hardware Used:
- Microcontroller (Raspberry Pi Pico or similar)
- 4x Servo motors
- 5x Push buttons (with pull-up configuration)
- SSD1306 OLED display (I2C)

Notes:
- Servo positions are updated incrementally based on button input
- PWM duty cycle is calculated from servo position values
- GPIO pins and I2C configuration may need adjustment depending on hardware setup
"""

def draw_status():
    write20.text("Servo Deg", 15, 0)
    oled.text("Servo 1:", 0, 25)
    oled.text(str(deg1), 66, 25)
    oled.text("Servo 2:", 0, 35)
    oled.text(str(deg2), 66, 35)
    oled.text("Servo 3:", 0, 45)
    oled.text(str(deg3), 66, 45)
    oled.text("Servo 4:", 0, 55)
    oled.text(str(deg4), 66, 55)
    oled.show()
    oled.fill(0)


show_startup_screen()

while True:
    draw_status()

    if button1.value() == 0:
        set_servo_cycle(servo1, deg1)
        deg1 = min(deg1 + 2, DEGREE_MAX)

    if button2.value() == 0:
        set_servo_cycle(servo3, deg3)
        set_servo_cycle(servo2, deg2)
        deg2 = min(deg2 + 5, DEGREE_MAX)
        deg3 = max(deg3 - 5, DEGREE_MIN)

    if button3.value() == 0:
        set_servo_cycle(servo1, deg1)
        deg1 = max(deg1 - 2, DEGREE_MIN)

    if button4.value() == 0:
        set_servo_cycle(servo3, deg3)
        set_servo_cycle(servo2, deg2)
        deg2 = max(deg2 - 5, DEGREE_MIN)
        deg3 = min(deg3 + 5, DEGREE_MAX)

    if button5.value() == 0:
        while button5.value() == 0:
            draw_status()
            set_servo_cycle(servo4, deg4)

            if gripper_direction == 0:
                deg4 = min(deg4 + 5, SERVO_4_MAX)
            else:
                deg4 = max(deg4 - 5, SERVO_4_MIN)

        gripper_direction = 1 - gripper_direction

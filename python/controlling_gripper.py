import RPi.GPIO as GPIO
import time

# GPIO pin connected to the gripper
GRIPPER_PIN = 18

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GRIPPER_PIN, GPIO.OUT)


def open_gripper():
    """Open the gripper"""
    GPIO.output(GRIPPER_PIN, GPIO.HIGH)
    print("Gripper is open")
    time.sleep(1)


def close_gripper():
    """Close the gripper"""
    GPIO.output(GRIPPER_PIN, GPIO.LOW)
    print("Gripper is closed")
    time.sleep(1)


if __name__ == "__main__":
    try:
        # Test gripper
        open_gripper()
        time.sleep(2)
        close_gripper()

    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting...")

    finally:
        GPIO.cleanup()

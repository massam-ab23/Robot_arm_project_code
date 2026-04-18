import RPi.GPIO as GPIO
import time

SERVO_PIN = 11
PWM_FREQUENCY = 50
MIN_DUTY = 2
MAX_DUTY = 17
STEP_DELAY = 1


def setup_servo():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    return GPIO.PWM(SERVO_PIN, PWM_FREQUENCY)


def sweep_servo(servo):
    print("Waiting for 1 second")
    time.sleep(1)

    print("Rotating at intervals")
    for duty in range(MIN_DUTY, MAX_DUTY + 1):
        servo.ChangeDutyCycle(duty)
        time.sleep(STEP_DELAY)

    print("Turning back to 0 degrees")
    servo.ChangeDutyCycle(MIN_DUTY)
    time.sleep(1)
    servo.ChangeDutyCycle(0)


def main():
    servo = setup_servo()
    try:
        servo.start(0)
        sweep_servo(servo)
    finally:
        servo.stop()
        GPIO.cleanup()
        print("Everything's cleaned up")


if __name__ == "__main__":
    main()

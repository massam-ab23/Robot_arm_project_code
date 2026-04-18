// Gripper control using Raspberry Pi GPIO (servo motor)

/*
Wiring:
Raspberry Pi 5V Pin  ------ Servo Red Wire
Raspberry Pi GND Pin ------ Servo Brown/Black Wire
Raspberry Pi GPIO Pin ----- Servo Orange/Yellow Wire (e.g., GPIO 18)
*/

#include <iostream>
#include <wiringPi.h>
#include <softPwm.h>
#include <unistd.h>

using namespace std;

// Define GPIO pin for servo control
const int SERVO_PIN = 18;  // Change if using a different GPIO pin

// Define PWM range (adjust as needed)
const int PWM_RANGE = 200;

// Function to open the gripper
void openGripper() {
    softPwmWrite(SERVO_PIN, 5);  // Adjust value for your servo
    delay(1000);                 // Wait 1 second
}

// Function to close the gripper
void closeGripper() {
    softPwmWrite(SERVO_PIN, 25); // Adjust value for your servo
    delay(1000);                 // Wait 1 second
}

int main() {
    // Initialize wiringPi (GPIO mode)
    if (wiringPiSetupGpio() == -1) {
        cerr << "Error setting up wiringPi." << endl;
        return 1;
    }

    // Initialize software PWM
    if (softPwmCreate(SERVO_PIN, 0, PWM_RANGE) != 0) {
        cerr << "Error setting up PWM." << endl;
        return 1;
    }

    char choice;

    while (true) {
        cout << "Enter 'o' to open gripper, 'c' to close gripper, or 'q' to quit: ";
        cin >> choice;

        if (choice == 'o') {
            openGripper();
        } else if (choice == 'c') {
            closeGripper();
        } else if (choice == 'q') {
            break;
        }
    }

    // Stop PWM before exiting
    softPwmWrite(SERVO_PIN, 0);

    return 0;
}

# PS4 Mouse for cool guyz :3

import pygame
import pyautogui
import sys

pyautogui.PAUSE = 0 # Stops the jittery mouse movement
pyautogui.FAILSAFE = False  # Disable PyAutoGUI fail-safe

# Initialize pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check for joystick connection
if pygame.joystick.get_count() == 0:
    print("No joystick connected")
    sys.exit()
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick connected: {joystick.get_name()}")

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Sensitivity settings
normal_sensitivity = 10  # Normal sensitivity
sprint_sensitivity = 20  # Sprint sensitivity
sneak_sensitivity = 5    # Sneak sensitivity
sensitivity = normal_sensitivity  # Current sensitivity

# Deadzone threshold
deadzone = 0.1

# Smoothing settings
smoothing_factor = 0.5
prev_x_axis = 0
prev_y_axis = 0

# Main loop
try:
    mouse_down = False  # Track the state of the left mouse button
    right_mouse_down = False  # Track the state of the right mouse button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get joystick axes
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)
        scroll_axis = joystick.get_axis(3)  # Right stick vertical axis

        # Apply deadzone
        if abs(x_axis) < deadzone:
            x_axis = 0
        if abs(y_axis) < deadzone:
            y_axis = 0
        if abs(scroll_axis) < deadzone:
            scroll_axis = 0

        # Apply smoothing
        x_axis = (x_axis * smoothing_factor) + (prev_x_axis * (1 - smoothing_factor))
        y_axis = (y_axis * smoothing_factor) + (prev_y_axis * (1 - smoothing_factor))
        prev_x_axis = x_axis
        prev_y_axis = y_axis

        # Adjust sensitivity based on R2 and L2 buttons
        r2_axis = joystick.get_axis(5)  # R2 button axis
        l2_axis = joystick.get_axis(4)  # L2 button axis

        if r2_axis > 0.5:  # R2 pressed
            sensitivity = sprint_sensitivity
            #print(f"Sensitivity set to sprint mode: {sensitivity}")
        elif l2_axis > 0.5:  # L2 pressed
            sensitivity = sneak_sensitivity
            #print(f"Sensitivity set to sneak mode: {sensitivity}")
        else:
            sensitivity = normal_sensitivity
            #print(f"Sensitivity set to normal mode: {sensitivity}")

        # Calculate mouse movement
        move_x = int(x_axis * sensitivity)
        move_y = int(y_axis * sensitivity)

        # Get current mouse position
        current_x, current_y = pyautogui.position()

        # Calculate new mouse position
        new_x = current_x + move_x
        new_y = current_y + move_y

        # Ensure the new position is within screen bounds
        new_x = max(0, min(screen_width - 1, new_x))
        new_y = max(0, min(screen_height - 1, new_y))

        # Check for left button presses
        if joystick.get_button(0):  # X button or button 0
            if not mouse_down:
                pyautogui.mouseDown(button='left')
                mouse_down = True
        else:
            if mouse_down:
                pyautogui.mouseUp(button='left')
                mouse_down = False

        # Check for right button presses
        if joystick.get_button(1):  # Circle button or button 1
            if not right_mouse_down:
                pyautogui.mouseDown(button='right')
                right_mouse_down = True
        else:
            if right_mouse_down:
                pyautogui.mouseUp(button='right')
                right_mouse_down = False

        # Move the mouse
        pyautogui.moveTo(new_x, new_y)

        # Scroll wheel functionality
        if scroll_axis != 0:
            pyautogui.scroll(int(scroll_axis * sensitivity))

        # Debug output for button presses
        # for i in range(joystick.get_numbuttons()):
        #     if joystick.get_button(i):
        #         print(f"Button {i} pressed")

        # Debug output
        #print(f"Joystick axes: ({x_axis:.2f}, {y_axis:.2f}) -> Mouse move: ({move_x}, {move_y}) -> New position: ({new_x}, {new_y})")

        # Small delay to prevent high CPU usage
        pygame.time.wait(10)

except KeyboardInterrupt:
    pygame.quit()
    sys.exit()
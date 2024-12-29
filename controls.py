from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from shared import buttons, hovered_button_index, pressed_button_index, showScreen, W_Width, W_Height, current_screen
from screens import play_action, help_action, shop_action

# Universal variables
mouse_x, mouse_y = 0, 0
character_x, character_y = W_Width // 2, W_Height // 2
bullets = []

'''I/O related functions'''

def mouseListener(button, state, x, y):
    """Handles mouse clicks for all screens."""
    global buttons, pressed_button_index, current_screen, mouse_x, mouse_y, bullets
    y = W_Height - y  # Convert mouse coordinates to OpenGL's system
    mouse_x, mouse_y = x, y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            # Check if any button is clicked
            for index, button_obj in enumerate(buttons):
                if button_obj.left <= x <= button_obj.left + button_obj.width and \
                   button_obj.bottom <= y <= button_obj.bottom + button_obj.height:
                    button_obj.is_pressed = True
                    pressed_button_index = index
                    print(f"Button '{button_obj.label}' pressed!")

            # If in game screen, handle shooting
            if current_screen == 3:
                bullets.append((character_x, character_y, mouse_x, mouse_y))

        elif state == GLUT_UP:
            # Handle button release actions
            if pressed_button_index != -1:
                buttons[pressed_button_index].is_pressed = False
                print(f"Button '{buttons[pressed_button_index].label}' released!")

                # Perform actions based on screen and button
                if current_screen == 0:  # Menu screen
                    if pressed_button_index == 0:  # Play button
                        current_screen = 3
                        play_action()
                    elif pressed_button_index == 1:  # Help button
                        current_screen = 1
                        help_action()
                    elif pressed_button_index == 2:  # Shop button
                        current_screen = 2
                        shop_action()
                elif current_screen in [1, 2]:  # Help or Shop screen
                    current_screen = 0
                    glutDisplayFunc(showScreen)
                    glutPostRedisplay()

                pressed_button_index = -1

    glutPostRedisplay()


def passiveMouseListener(x, y):
    """Handles mouse hovering for all screens."""
    global buttons, hovered_button_index, mouse_x, mouse_y
    y = W_Height - y  # Convert mouse coordinates to OpenGL's system
    mouse_x, mouse_y = x, y

    new_hovered_button_index = -1

    for index, button in enumerate(buttons):
        # Check if the mouse is within the button's bounds
        if button.left <= x <= button.left + button.width and button.bottom <= y <= button.bottom + button.height:
            button.is_hovered = True
            new_hovered_button_index = index
        else:
            button.is_hovered = False

    # Trigger re-render if hover state changes
    if new_hovered_button_index != hovered_button_index:
        hovered_button_index = new_hovered_button_index
        glutPostRedisplay()


def keyboardListener(key, x, y):
    """Handles keyboard input for all screens."""
    global character_x, character_y

    movement_speed = 10

    # Handle game-specific controls
    if current_screen == 3:
        if key == b'w' and character_y + 25 < W_Height:
            character_y += movement_speed
        elif key == b's' and character_y - 25 > 0:
            character_y -= movement_speed
        elif key == b'a' and character_x - 20 > 0:
            character_x -= movement_speed
        elif key == b'd' and character_x + 20 < W_Width:
            character_x += movement_speed
    else:
        # Handle menu-specific controls if needed
        pass

    glutPostRedisplay()

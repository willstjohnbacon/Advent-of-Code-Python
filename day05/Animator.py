from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.renderers import StaticRenderer
from asciimatics.paths import Path
from asciimatics.effects import Print

from Dock import Dock
from Crane import Crane
from MovingCraneTrolley import MovingCraneTrolley
from MovingCraneHoist import MovingCraneHoist
from MovingCrate import MovingCrate

NONE = 0
LIFT = 1
ALIGN = 2
DROP = 3

# KEYPRESS_BETWEEN_MOVES = -1    # if TESTING else 0  # -1 for YES, 0 for NO
KEYPRESS_BETWEEN_MOVES = 0
MOVEMENT_SPEED_FACTOR = 3
INITIAL_FRAMES = 10

DOCK_OFFSET = 10    # if TESTING else 3
# DOCK_OFFSET = 3
LABEL_OFFSET = 1
COMMENTARY_OFFSET = 1
MAX_LIFT_HEIGHT = (30 - DOCK_OFFSET)    # if TESTING else (9 - DOCK_OFFSET)
# MAX_LIFT_HEIGHT = (9 - DOCK_OFFSET)
CRANE_TOP = MAX_LIFT_HEIGHT - 5
CRANE_CLEARANCE = 20
TROLLEY_HEIGHT = CRANE_TOP + 3


class Animator:
    def __init__(self, screen, stacks):
        self.screen = screen
        self.scenes = []

        self.dock_width = len(stacks) * 4
        self.dock_left = (self.screen.width - self.dock_width) // 2
        self.dock_floor = self.screen.height - DOCK_OFFSET

        self.trolley_pos = self.trolley_pos = self.dock_left - (CRANE_CLEARANCE // 2)

    def play(self, stop_on_resize=True, repeat=False):
        self.screen.play(self.scenes, stop_on_resize=stop_on_resize, repeat=repeat)

    def add_scene(self, description, movement, stacks, crane_stack, num_crates, from_stack, to_stack):
        max_stack_height = max(map(len, stacks))
        stacks_top = self.dock_floor - max_stack_height

        if movement == NONE:
            effects = [self.print_description(description),
                       self.print_stacks(stacks_top, stacks)]

            self.scenes.append(Scene(effects, clear=False, duration=-1))
            return

        stack = stacks[from_stack if movement == LIFT else to_stack]
        stack_height = len(stack)

        if movement == LIFT:
            crate = stack[stack_height - 1]
            crate_start_pos_x = self.dock_left + (from_stack * 4)
            crate_start_pos_y = self.dock_floor - LABEL_OFFSET - stack_height
            crate_end_pos_x = crate_start_pos_x
            crate_end_pos_y = MAX_LIFT_HEIGHT + len(crane_stack)
            crate_movement_steps = abs(crate_start_pos_y - crate_end_pos_y)
            crate_path = calculate_path(crate_start_pos_x, crate_start_pos_y, crate_end_pos_x, crate_end_pos_y,
                                        crate_movement_steps)

            # Trolley moves above crate to be lifted
            trolley_steps = abs(crate_start_pos_x - self.trolley_pos) // MOVEMENT_SPEED_FACTOR
            trolley_path = calculate_path(self.trolley_pos, TROLLEY_HEIGHT, crate_start_pos_x, TROLLEY_HEIGHT,
                                          trolley_steps)

            hoist_steps = crate_movement_steps
            hoist_down_path = calculate_path(crate_start_pos_x, crate_end_pos_y - 1, crate_start_pos_x,
                                             crate_start_pos_y - 1, hoist_steps)
            hoist_up_path = calculate_path(crate_start_pos_x, crate_start_pos_y - 1, crate_start_pos_x,
                                           crate_end_pos_y - 1, hoist_steps)

            first_trolley_frame = INITIAL_FRAMES
            final_trolley_frame = first_trolley_frame + (trolley_steps * MOVEMENT_SPEED_FACTOR)
            first_hoist_down_frame = final_trolley_frame
            final_hoist_down_frame = first_hoist_down_frame + (hoist_steps * MOVEMENT_SPEED_FACTOR)
            first_crate_frame = final_hoist_down_frame
            final_crate_frame = first_crate_frame + (crate_movement_steps * MOVEMENT_SPEED_FACTOR)
            first_hoist_up_frame = final_hoist_down_frame
            final_hoist_up_frame = first_hoist_up_frame + (hoist_steps * MOVEMENT_SPEED_FACTOR)

        elif movement == DROP:
            crate = crane_stack[len(crane_stack) - 1]
            crate_start_pos_x = self.dock_left + (to_stack * 4)
            crate_start_pos_y = MAX_LIFT_HEIGHT + len(crane_stack) - 1
            crate_end_pos_x = crate_start_pos_x
            crate_end_pos_y = self.dock_floor - LABEL_OFFSET - stack_height - 1
            crate_movement_steps = abs(crate_start_pos_y - crate_end_pos_y)
            crate_path = calculate_path(crate_start_pos_x, crate_start_pos_y, crate_end_pos_x, crate_end_pos_y,
                                        crate_movement_steps)

            # Trolley does not move
            trolley_steps = 0
            trolley_path = calculate_path(crate_end_pos_x, TROLLEY_HEIGHT, crate_end_pos_x, TROLLEY_HEIGHT,
                                          trolley_steps)

            hoist_steps = crate_movement_steps
            hoist_down_path = calculate_path(crate_end_pos_x, crate_start_pos_y - 1, crate_end_pos_x,
                                             crate_end_pos_y - 1, hoist_steps)
            hoist_up_path = calculate_path(crate_end_pos_x, crate_end_pos_y - 1, crate_end_pos_x, crate_start_pos_y - 1,
                                           hoist_steps)

            first_trolley_frame = 0
            final_trolley_frame = 1
            first_hoist_down_frame = INITIAL_FRAMES
            final_hoist_down_frame = first_hoist_down_frame + (hoist_steps * MOVEMENT_SPEED_FACTOR)
            first_crate_frame = first_hoist_down_frame
            final_crate_frame = first_crate_frame + (crate_movement_steps * MOVEMENT_SPEED_FACTOR)
            first_hoist_up_frame = final_hoist_down_frame
            final_hoist_up_frame = first_hoist_up_frame + (hoist_steps * MOVEMENT_SPEED_FACTOR)

        else:  # ALIGN
            crate = crane_stack[len(crane_stack) - 1]
            crate_start_pos_x = self.dock_left + (from_stack * 4)
            crate_start_pos_y = MAX_LIFT_HEIGHT + len(crane_stack) - 1
            crate_end_pos_x = self.dock_left + (to_stack * 4)
            crate_end_pos_y = crate_start_pos_y
            crate_movement_steps = abs(crate_start_pos_x - crate_end_pos_x) // MOVEMENT_SPEED_FACTOR
            crate_path = calculate_path(crate_start_pos_x, crate_start_pos_y, crate_end_pos_x, crate_end_pos_y,
                                        crate_movement_steps)

            # Trolley moves above stack on which crate is to be dropped
            trolley_steps = abs(crate_start_pos_x - crate_end_pos_x) // MOVEMENT_SPEED_FACTOR
            trolley_path = calculate_path(crate_start_pos_x, TROLLEY_HEIGHT, crate_end_pos_x, TROLLEY_HEIGHT,
                                          trolley_steps)

            # Hoist does not move
            hoist_steps = 0
            hoist_down_path = calculate_path(crate_end_pos_x, TROLLEY_HEIGHT + 1, crate_end_pos_x, TROLLEY_HEIGHT + 1,
                                             hoist_steps)
            hoist_up_path = hoist_down_path

            first_trolley_frame = INITIAL_FRAMES
            final_trolley_frame = first_trolley_frame + (trolley_steps * MOVEMENT_SPEED_FACTOR)
            first_hoist_down_frame = final_trolley_frame
            final_hoist_down_frame = final_trolley_frame
            first_crate_frame = first_trolley_frame
            final_crate_frame = first_crate_frame + (crate_movement_steps * MOVEMENT_SPEED_FACTOR)
            first_hoist_up_frame = final_trolley_frame
            final_hoist_up_frame = final_trolley_frame

        self.trolley_pos = crate_end_pos_x

        effects = [
            self.print_description(description),
            self.print_crane(),
            self.print_stacks(stacks_top, stacks),
            MovingCraneTrolley(self.screen, trolley_path, start_frame=first_trolley_frame,
                               stop_frame=final_trolley_frame),
            MovingCraneHoist(self.screen, hoist_up_path, start_frame=first_hoist_up_frame,
                             stop_frame=final_hoist_up_frame),
            MovingCrate(self.screen, crate_path, f"[{crate}]", start_frame=first_crate_frame,
                        stop_frame=final_crate_frame),
            MovingCraneHoist(self.screen, hoist_down_path, moving_up=False, start_frame=first_hoist_down_frame,
                             stop_frame=final_hoist_down_frame),
        ]

        self.scenes.append(
            Scene(effects, clear=False, duration=KEYPRESS_BETWEEN_MOVES if movement == DROP else 0))

    def print_crane(self):
        crane_left = self.dock_left - CRANE_CLEARANCE

        return Print(
            self.screen,
            Crane(crane_left, self.dock_floor, self.dock_width, CRANE_TOP, CRANE_CLEARANCE),
            x=crane_left, y=CRANE_TOP,
            colour=Screen.COLOUR_YELLOW,
            clear=False,
            start_frame=0,
            stop_frame=5)

    def print_stacks(self, stacks_top, stacks):
        return Print(
            self.screen,
            Dock(stacks),
            x=self.dock_left - 1, y=stacks_top - 1,
            colour=Screen.COLOUR_CYAN,
            clear=False,
            start_frame=0,
            stop_frame=5)

    def print_description(self, description):
        x_pos = (self.screen.width - len(description)) // 2 - 1

        return Print(
            self.screen,
            StaticRenderer([description]),
            x=x_pos, y=self.dock_floor + COMMENTARY_OFFSET,
            colour=Screen.COLOUR_WHITE,
            clear=False,
            transparent=False,
            start_frame=0,
            stop_frame=5)


def calculate_path(start_pos_x, start_pos_y, end_pos_x, end_pos_y, steps):
    path = Path()
    path.jump_to(start_pos_x, start_pos_y)
    path.move_straight_to(end_pos_x, end_pos_y, steps)
    path.wait(100)
    return path

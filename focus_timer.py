from time import time, sleep
from curses import initscr, newwin, curs_set, cbreak, noecho, nocbreak, echo, endwin, A_NORMAL, A_UNDERLINE, A_STANDOUT
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from playsound import playsound
from os.path import split, join
from sys import argv, exit

class Timer:
    def __init__(self, total_time) -> None:
        self.total_time = total_time
        self.remaining_time = total_time
        self.start_time = None
        self.running = False

    def __str__(self) -> None:
        remaining = self.get_remaining_time()
        minutes, seconds = divmod(round(remaining), 60)
        return f"{int(minutes):02}:{int(seconds):02}"

    def start(self) -> None:
        if not self.running:
            self.start_time = time()
            self.running = True

    def stop(self) -> None:
        if self.running:
            elapsed_time = time() - self.start_time
            self.remaining_time -= elapsed_time
            self.running = False

    def reset(self) -> None:
        self.remaining_time = self.total_time
        self.start_time = None
        self.running = False

    def get_remaining_time(self) -> float:
        if self.running:
            elapsed_time = time() - self.start_time
            return max(self.remaining_time - elapsed_time, 0)
        return max(self.remaining_time, 0)

    def is_finished(self) -> None:
        return self.get_remaining_time() == 0

class Renderer:
    def __init__(self, intervals, footer_list) -> None:
        # INIT WINDOWS
        self.screen = initscr()
        dimensions = self.screen.getmaxyx()
        clock_x, clock_y = self.get_coordinates_for_centered_text(" "*5)
        text_x, text_y = self.get_coordinates_for_centered_text(" "*10)
        interval_x, interval_y = self.get_coordinates_for_centered_text(" "*(len(str(intervals))*2+2))
        self.windows = [self.screen, # 0: main_scr
                        newwin(1, dimensions[1], dimensions[0]-1, 0), # 1: footer
                        newwin(1, 6, clock_y, clock_x), # 2: clock
                        newwin(1, 11, text_y-1, text_x), # 3: text above clock
                        newwin(1, len(str(intervals))*2+2, interval_y+1, interval_x+1)] # 4: interval x/N

        # ADJUST SETTINGS
        curs_set(0)
        cbreak()
        noecho()
        self.screen.nodelay(True)
        self.screen.keypad(True)

        # CLEAR SCREEN
        self.screen.clear()
        self.screen.refresh()

        # PRINT FOOTER TO WINDOW
        self.init_footer(footer_list, dimensions[1]-1)

    def init_footer(self, args: list, max_len: int) -> None:
        char_amount = len("".join(args))

        if char_amount < max_len:
            width = (max_len - char_amount) // (len(args) - 1)
            formatted_string = "".join([arg + " "*width for arg in args]).strip()
            if self.windows[1].getbegyx()[0] >= self.windows[4].getbegyx()[0]:
                self.output_text_to_window(1, formatted_string, 0, 0)
            return

        if char_amount // 2 < max_len:
            self.change_footer()
            lists = args[:len(args)//2], args[len(args)//2:]
            char_amount_1 = len("".join(lists[0]))
            char_amount_2 = len("".join(lists[1]))
            width_1 = (max_len - char_amount_1) // (len(lists[0])-1)
            width_2 = (max_len - char_amount_2) // (len(lists[1])-1)
            lists = ["".join([arg + " "*width_1 for arg in lists[0]]).strip(), "".join([arg + " "*width_2 for arg in lists[1]]).strip()]
            if self.windows[1].getbegyx()[0] >= self.windows[4].getbegyx()[0]:
                self.output_text_to_window(1, lists[0], 0, 0)
                self.output_text_to_window(1, lists[1], 1, 0)
            return

    def change_footer(self) -> None:
        dimensions = self.screen.getmaxyx()
        self.windows[1] = newwin(2, dimensions[1], dimensions[0]-2, 0)

    def output_text_to_window(self, win: int, text: str, y=0, x=0, *args) -> None:
        error_msg = "Couldn't print string to window."
        attributes = A_NORMAL
        for attr in args:
            attributes |= attr
        try:
            self.windows[win].addstr(y, x, text, attributes)
        except Exception:
            print(error_msg)
        self.windows[win].refresh()

    def get_input(self) -> str:
        try:
            return self.screen.getkey()
        except:
            return None

    def get_coordinates_for_centered_text(self, text: str) -> tuple[int]:
        height, width = self.screen.getmaxyx()
        start_y = height // 2
        start_x = (width // 2) - (len(text) // 2)
        return start_x, start_y-1

    def kill_scr(self) -> None:
        nocbreak()
        self.screen.keypad(False)
        echo()
        endwin()

def main(args):
    # Init Objects
    footer_list = ["[P]ause/[C]ontinue", "[R]eset", "[U]pdate", "[Q]uit"]
    screen = Renderer(args.intervals, footer_list)
    timer = [Timer(60*args.worktime), Timer(60*args.breaktime)]

    def run_prog():
        current_interval = 0
        nonlocal screen
        title = ["Focus Time", "Break Time"]
        break_timer_enabled = False
        for i in range(args.intervals*2-1):
            if i%2==0: current_interval+=1
            screen.output_text_to_window(4, f"{current_interval:0{len(str(args.intervals))}}/{args.intervals}", 0, 0)
            screen.output_text_to_window(3, title[break_timer_enabled], 0, 0, A_UNDERLINE)
            current_timer = timer[break_timer_enabled]
            current_timer.reset()
            current_timer.start()
            while not current_timer.is_finished():
                sleep(0.1)
                if (key:=screen.get_input()) != None: key = key.upper()
                match key:
                    case "Q":
                        screen.kill_scr()
                        exit()
                    case "P" | "C":
                        if current_timer.running:
                            current_timer.stop()
                        else:
                            current_timer.start()
                    case "R":
                        timer[0].reset()
                        timer[1].reset()
                        screen.output_text_to_window(4, f"{1:0{len(str(args.intervals))}}/{args.intervals}", 0, 0)
                        screen.output_text_to_window(3, title[0], 0, 0, A_UNDERLINE)
                        screen.output_text_to_window(2, timer[0].__str__(), 0, 0, A_STANDOUT)
                        sleep(3)
                        run_prog()
                    case "U" | "KEY_RESIZE":
                        screen.kill_scr()
                        screen = Renderer(args.intervals, footer_list)
                        screen.output_text_to_window(4, f"{current_interval:0{len(str(args.intervals))}}/{args.intervals}", 0, 0)
                        screen.output_text_to_window(3, title[break_timer_enabled], 0, 0, A_UNDERLINE)
                        screen.output_text_to_window(2, current_timer.__str__(), 0, 0, A_STANDOUT)

                screen.output_text_to_window(2, current_timer.__str__(), 0, 0, A_STANDOUT)

            file = "sound.mp3"
            filepath = join(split(argv[0])[0], file)
            try:
                with StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
                    playsound(filepath, False)
                sleep(3)
            except Exception:
                print(f"Something went wrong with playing the {file} file. Make shure it exists in the folder of this python file.\n{split(argv[0])[0]}")
                sleep(3)

            break_timer_enabled = 1 - break_timer_enabled

    run_prog()

    screen.kill_scr()

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="Focus Timer",
                            description="A basic focus timer which uses an interval of work and pause time to maximise productivity.",
                            epilog="Have fun using it =)")

    parser.add_argument("intervals", type=int, help="Number of focus sessions wanted")
    parser.add_argument("-w", "--worktime",
                        default=25,
                        nargs="?",
                        const=25,
                        type=float,
                        help="Time spend working on the task in minutes. Defaults to 25 minutes.")
    parser.add_argument("-b", "--breaktime",
                        default=5,
                        nargs="?",
                        const=5,
                        type=float,
                        help="Length of the break between the focus sessions in minutes. Defaults to 5 minutes.")

    args = parser.parse_args()

    main(args)

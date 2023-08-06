import argparse
import curses
import datetime
import locale
import os
import signal
import textwrap
import time
from concurrent import futures

import blessings
import datefinder

from pylogview.__version__ import __version__

locale.setlocale(locale.LC_ALL, "")

APPLICATION_TITLE = "logview"

DELIMETERS = [" - ", " | "]

MAX_COLS = 3
MAX_ROWS = 4
MAX_WINS = MAX_COLS * MAX_ROWS
ACTIVE_DELAY = 10
LOOP_MS = 50

BLK_T = "\u2580"
BLK_B = "\u2584"
BLK = "\u2588"
BLK_L = "\u258C"
BLK_R = "\u2590"
BLK_BL = "\u2599"
BLK_TL = "\u259B"
BLK_TR = "\u259C"
BLK_BR = "\u259F"

APP_FG = 0
APP_BG = 1
APP_FRAME = 2
APP_TITLE = 3
APP_CLOCK = 4
WIN_FRAME = 5
WIN_FRAME_ACTIVE = 6
WIN_FRAME_SELECT = 7
WIN_FRAME_SELECT_ACTIVE = 8
WIN_FRAME_LOAD = 9
WIN_FRAME_ERROR = 10
WIN_TITLE = 11
WIN_LINES = 12
LOG_LEVEL = {"DEBUG": 13, "INFO": 14, "WARNING": 15, "WARN": 15, "ERROR": 16}
LOG_FG = 17
LOG_FG_DARK = 18
LOG_BG = 19
# fmt: off
COLORS = {
    16: [
        15, # APP_FG
        16, # APP_BG
        4,  # APP_FRAME
        3,  # APP_TITLE
        16, # APP_CLOCK
        2,  # WIN_FRAME
        10, # WIN_FRAME_ACTIVE
        6,  # WIN_FRAME_SELECT
        14, # WIN_FRAME_SELECT_ACTIVE
        3,  # WIN_FRAME_LOAD
        1,  # WIN_FRAME_ERROR
        16, # WIN_TITLE
        16, # WIN_LINES
        8,  # LOG_LEVEL: DEBUG
        10, # LOG_LEVEL: INFO
        11, # LOG_LEVEL: WARN
        9,  # LOG_LEVEL: ERROR
        15, # LOG_FG
        8,  # LOG_FG_DARK
        16, # LOG_BG
    ],
    88: [
        15, # APP_FG
        16, # APP_BG
        4,  # APP_FRAME
        3,  # APP_TITLE
        16, # APP_CLOCK
        28, # WIN_FRAME
        46, # WIN_FRAME_ACTIVE
        6,  # WIN_FRAME_SELECT
        45, # WIN_FRAME_SELECT_ACTIVE
        3,  # WIN_FRAME_LOAD
        1,  # WIN_FRAME_ERROR
        16, # WIN_TITLE
        16, # WIN_LINES
        8,  # LOG_LEVEL: DEBUG
        40, # LOG_LEVEL: INFO
        11, # LOG_LEVEL: WARN
        9,  # LOG_LEVEL: ERROR
        15, # LOG_FG
        8,  # LOG_FG_DARK
        16, # LOG_BG
    ],
    256: [
        15, # APP_FG
        16, # APP_BG
        4,  # APP_FRAME
        3,  # APP_TITLE
        16, # APP_CLOCK
        28, # WIN_FRAME
        46, # WIN_FRAME_ACTIVE
        6,  # WIN_FRAME_SELECT
        45, # WIN_FRAME_SELECT_ACTIVE
        3,  # WIN_FRAME_LOAD
        1,  # WIN_FRAME_ERROR
        16, # WIN_TITLE
        16, # WIN_LINES
        246,# LOG_LEVEL: DEBUG
        40, # LOG_LEVEL: INFO
        208,# LOG_LEVEL: WARN
        9,  # LOG_LEVEL: ERROR
        15, # LOG_FG
        240,# LOG_FG_DARK
        233,# LOG_BG
    ]
}
# fmt: on

config = None
windows = []
colors = []
log = []


class Window(object):
    def __init__(self, filename):
        self.filename = filename
        self.name = os.path.split(filename)[-1]
        self.fd = None
        self.term = None
        self._selected = False
        self.active_delay = 0
        self._last_line = 0
        self._display_lines = []
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.frame = colors[WIN_FRAME_LOAD]
        self.lines = []
        self.count = 0
        try:
            self.fd = open(self.filename, "rb")
        except:
            log.append(f"Failed to open '{self.filename}'")
            self.fd = None

    def __del__(self):
        if self.fd:
            self.fd.close()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        if value:
            self.frame = colors[
                WIN_FRAME_SELECT_ACTIVE if self.active_delay else WIN_FRAME_SELECT
            ]
        else:
            self.frame = colors[WIN_FRAME_ACTIVE if self.active_delay else WIN_FRAME]

    def scroll_up(self, lines=1):
        if self._last_line > 0 - len(self.lines) + 1:  # + (self.h - 2):
            self._last_line -= lines
            self.select_lines()

    def scroll_down(self, lines=1):
        if self._last_line < 0:
            self._last_line += lines
            self.select_lines()

    def scroll_end(self):
        if self._last_line < 0:
            self._last_line = 0
            self.select_lines()

    def page_up(self):
        self.scroll_up(5)

    def page_down(self):
        self.scroll_down(5)

    def start(self, term):
        self.term = term
        self.draw_frame(True)

    def load(self):
        if self.fd:
            self.read_count()
        if self.fd:
            self.read_last(config.lines)
        if self.fd:
            self.data = self.fd.read()
            self.select_lines()
            self.frame = colors[WIN_FRAME_SELECT if self.selected else WIN_FRAME]

    def draw_frame(self, fill=False):
        tprint(  # draw top edge and corners
            self.term,
            self.term.move(self.y, self.x),
            self.term.color(self.frame) + self.term.on_color(colors[LOG_BG]),
            BLK * int((self.w - len(self.name)) / 2),
            self.term.color(colors[WIN_TITLE]) + self.term.on_color(self.frame),
            self.term.bold,
            self.name,
            self.term.color(self.frame) + self.term.on_color(colors[LOG_BG]),
            BLK
            * int(
                (
                    ((self.w - len(self.name)) / 2)
                    + (((self.w - len(self.name)) / 2) % 1)
                )
                - 18
            ),
            self.term.color(colors[WIN_LINES]),
            self.term.on_color(self.frame),
            self.term.bold,
            f"lines: {locale.format_string('%d', self.count, True):>9}",
            self.term.color(self.frame) + self.term.on_color(colors[LOG_BG]),
            BLK * 2,
        )
        tprint(  # draw bottom edge and corners
            self.term,
            self.term.move(self.y + self.h - 1, self.x),
            self.term.color(self.frame) + self.term.on_color(colors[LOG_BG]),
            BLK_BL,
            BLK_B * (self.w - 2),
            BLK_BR,
        )
        # draw left and right edge and fill window
        tformat(self.term.color(self.frame) + self.term.on_color(colors[LOG_BG]))
        if fill:
            for row in range(self.y + 1, self.y + self.h - 1):
                print(
                    self.term.move(row, self.x) + BLK_L + (" " * (self.w - 2)) + BLK_R
                )
        else:
            for row in range(self.y + 1, self.y + self.h - 1):
                print(
                    self.term.move(row, self.x)
                    + BLK_L
                    + self.term.move(row, self.x + self.w - 1)
                    + BLK_R
                )
        # reset formatting
        tprint(self.term)

    def refresh(self, force=False):
        new_data = self.read()
        if new_data and not force:
            self.active_delay = ACTIVE_DELAY
            self.frame = colors[
                WIN_FRAME_SELECT_ACTIVE if self._selected else WIN_FRAME_ACTIVE
            ]
            self.select_lines()

        if new_data or force:
            self.draw_frame()
            tformat(self.term.on_color(colors[LOG_BG]))
            for i in range(len(self._display_lines)):
                print(
                    self.term.move(self.y + i + 1, self.x + 1)
                    + (" " * (self.w - 2))
                    + self.term.move(self.y + i + 1, self.x + 1)
                    + self._display_lines[i]
                )

        if self._last_line == 0 and not new_data:
            if self.active_delay > 0:
                self.active_delay -= 1
            else:
                new_frame = colors[WIN_FRAME_SELECT if self._selected else WIN_FRAME]
                if self.frame != new_frame:
                    self.frame = new_frame
                    self.draw_frame()
                else:
                    self.frame = new_frame

    def select_lines(self):
        lines = []
        for line in range(self.h - 1, 0, -1):
            if len(self.lines) + (self._last_line - line) >= 0:
                lines.extend(
                    self.format_line(
                        self.lines[len(self.lines) + (self._last_line - line)]
                    )
                )
            else:
                lines.append("")
        lines = lines[2 - self.h :]
        lines = lines + [""] * (self.h - 2 - len(lines))
        self._display_lines = lines

    def format_line(self, s):
        if config.trim_date:
            # search for timestamp and replace with HH:MM:SS.FFF
            dt = [*datefinder.find_dates(s, source=True)]
            if dt:
                dt = dt[0]
                stime = dt[0].strftime("%H:%M:%S.%f")[:-3]
                s = s.replace(dt[1], stime, 1)
        # search for log level
        level_key = None
        level_color = self.term.color(colors[LOG_FG])
        for key in LOG_LEVEL.keys():
            if key in s:
                level_key = key
                level_color = self.term.color(colors[LOG_LEVEL[key]])
                break
        # break line at header/message delimeter if it is past 50% width
        lines = []
        for delim in DELIMETERS:
            delim_pos = s.find(delim)
            if delim_pos >= (self.w - 2) // 2 and delim_pos < self.w - 2:
                lines.append(s[: delim_pos + len(delim)])
                lines.append(f"{s[delim_pos + len(delim) :]}")
                break
        delim_pos = -1
        # wrap line
        if lines:
            lines.extend(
                textwrap.wrap(
                    lines[1].lstrip(),
                    width=self.w - 2,
                    initial_indent="  ",
                    subsequent_indent="  ",
                )
            )
            lines.pop(1)
        else:
            lines = textwrap.wrap(s, width=self.w - 2, subsequent_indent="  ")
        # add formatting
        #   darken from start
        lines[0] = f"{self.term.color(colors[LOG_FG_DARK])}{lines[0]}"
        #   highlight log level
        if level_key:
            level_pos = lines[0].find(level_key)
            lines[0] = (
                f"{lines[0][:level_pos]}"
                f"{level_color}{self.term.bold}{lines[0][level_pos : level_pos + len(level_key)]}"
                f"{self.term.normal}{self.term.on_color(colors[LOG_BG])}"
                f"{self.term.color(colors[LOG_FG_DARK])}{lines[0][level_pos + len(level_key):]}"
            )
        #   level FG after delimiter
        for delim in DELIMETERS:
            delim_pos = lines[0].find(delim)
            if delim_pos >= 0:
                lines[0] = (
                    f"{lines[0][:delim_pos + len(delim)]}"
                    f"{level_color}"
                    f"{lines[0][delim_pos + len(delim):]}"
                )
                break
        # add level FG to all split lines
        for line in range(1, len(lines)):
            lines[line] = f"{level_color}{lines[line]}"
        # return formatted lines
        return lines

    def read(self):
        """Read to end of file and parse next line"""
        if not self.fd.closed:
            try:
                self.data += self.fd.read()
                nl = self.data.find(b"\n")
                if nl >= 0:
                    self.lines.append(self.data[:nl].strip(bytes(0)).decode())
                    self.lines = self.lines[0 - config.lines :]
                    self.data = self.data[nl + 1 :]
                    self.count += 1
                    if self._last_line < -1:
                        self.scroll_up()
                    return True
            except IOError:
                pass
        return False

    def read_count(self):
        try:
            self.fd.seek(0, 0)
            self.count = 0
            for line in self.fd:  # pylint: disable=unused-variable
                self.count += 1
        except IOError as err:
            self.fd = None
            print(
                self.term.move(self.y + 1, self.x + 1)
                + self.term.color(colors[LOG_FG])
                + self.term.on_color(colors[LOG_BG])
                + "An I/O error occured while reading line count"
            )
            i = 2
            for line in textwrap.wrap(
                f"[{err.errno}] {err.strerror}",
                width=self.w - 2,
                subsequent_indent=2,
            ):
                print(self.term.move(self.y + i, self.x + 1) + line)
                i += 1
            self.frame = colors[WIN_FRAME_ERROR]
            self.count = 0
            self.draw_frame()

    def read_last(self, lines):
        """Read last ``lines`` of file, like 'tail -n'"""
        try:
            last_read_block = self.fd.tell()
            block_end_byte = last_read_block
            BLOCK_SIZE = min(block_end_byte, 1024)
            remain_lines = lines
            block_num = -1
            blocks = []
            while remain_lines > 0 and block_end_byte > 0:
                if block_end_byte - BLOCK_SIZE > 0:
                    self.fd.seek(block_num * BLOCK_SIZE, 2)
                    blocks.append(self.fd.read(BLOCK_SIZE))
                else:
                    self.fd.seek(0, 0)
                    blocks.append(self.fd.read(block_end_byte))
                remain_lines -= blocks[-1].count(b"\n")
                block_end_byte -= BLOCK_SIZE
                block_num -= 1
            self.fd.seek(last_read_block, 0)
        except IOError as err:
            self.fd = None
            print(
                self.term.move(self.y + 1, self.x + 1)
                + self.term.color(colors[LOG_FG])
                + self.term.on_color(colors[LOG_BG])
                + "An I/O error occured while reading tail lines"
            )
            i = 2
            for line in textwrap.wrap(
                f"[{err.errno}] {err.strerror}",
                width=self.w - 2,
                subsequent_indent=2,
            ):
                print(self.term.move(self.y + i, self.x + 1) + line)
                i += 1
            self.frame = colors[WIN_FRAME_ERROR]
            self.draw_frame()
        else:
            self.lines.extend(
                b"".join(blocks[::-1]).strip(bytes(0)).decode().splitlines()[-lines:]
            )


class SignalHook:
    """
    Hooks to SIGINT, SIGTERM, SIGKILL
    """

    SIGINT = signal.SIGINT
    SIGTERM = signal.SIGTERM
    SIGKILL = signal.SIGKILL

    def __init__(self):
        self._last_signal = None
        try:
            signal.signal(signal.SIGINT, self._signal_received)
        except OSError:
            pass
        try:
            signal.signal(signal.SIGTERM, self._signal_received)
        except OSError:
            pass
        try:
            signal.signal(signal.SIGKILL, self._signal_received)
        except OSError:
            pass

    def _signal_received(self, signum, frame):
        self._last_signal = signal.Signals(signum)  # pylint: disable=no-member

    @property
    def signal(self):
        return self._last_signal

    @property
    def exit(self):
        return self._last_signal in [self.SIGINT, self.SIGTERM, self.SIGKILL]


def parse_args():
    parser = argparse.ArgumentParser(
        prog="logview", description="logview allows you to tail multiple files at once"
    )
    parser.add_argument(
        "-t",
        "--trim-date",
        action="store_true",
        help="display only time from timestamp",
    )
    parser.add_argument(
        "-n",
        "--lines",
        metavar="NUM",
        type=int,
        default=1000,
        help="scrollback buffer lines (default 1000)",
    )
    parser.add_argument(
        "-d",
        "--dir",
        default="",
        help="directory to find FILE(s) in",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show version number and exit",
    )
    parser.add_argument(
        "file", metavar="FILE", nargs="+", help=f"file(s) to tail, maximum {MAX_WINS}"
    )
    return parser.parse_args()


def tprint(term, *s):
    if len(s) == 0:
        print(term.move(0, 0) + term.normal)
    else:
        print(*s, sep="", end=term.normal)


def tformat(*s):
    print(sep="", end="".join(s))


def draw_app(term):
    top_before_title = int((term.width - len(APPLICATION_TITLE)) / 2)
    top_after_title = int(
        ((term.width - len(APPLICATION_TITLE)) / 2)
        + (((term.width - len(APPLICATION_TITLE)) / 2) % 1)
        - 12  # clock space
    )
    tprint(
        term,
        term.move(0, 0),
        term.color(colors[APP_FRAME]),
        term.on_color(colors[APP_BG]),
        BLK * top_before_title,
        term.color(colors[APP_TITLE]),
        term.on_color(colors[APP_FRAME]),
        term.bold,
        APPLICATION_TITLE,
        term.color(colors[APP_FRAME]),
        term.on_color(colors[APP_BG]),
        BLK * top_after_title,
        term.color(colors[APP_CLOCK]),
        term.on_color(colors[APP_FRAME]),
        term.bold,
        datetime.datetime.now().strftime("%H:%M:%S"),
        term.color(colors[APP_FRAME]),
        term.on_color(colors[APP_BG]),
        BLK * 4,
        term.move(term.height - 1, 0),
        # BLK * term.width,
        term.color(colors[APP_CLOCK]),
        term.on_color(colors[APP_FRAME]),
        "TAB: Next Window   SPACE: Jump to end   Q: Quit".center(term.width),
    )
    tformat(term.color(colors[APP_FRAME]), term.on_color(colors[APP_BG]))
    for row in range(1, term.height - 1):
        print(term.move(row, 0) + BLK + term.move(row, term.width - 1) + BLK)
    tprint(term)


def draw_clock(term):
    tprint(
        term,
        term.move(0, term.width - 12),
        term.color(colors[APP_CLOCK]),
        term.on_color(colors[APP_FRAME]),
        term.bold,
        datetime.datetime.now().strftime("%H:%M:%S"),
    )


def calculate_windows(term):
    col_count = 1
    row_count = 1
    row_limit = 1
    while len(windows) / col_count / row_count > 1:
        if row_count == row_limit:
            row_count = 1
            row_limit += 1
            col_count += 1 if col_count < MAX_COLS else 0
        else:
            row_count += 1

    win_width = int((term.width - 2) / col_count)
    for col in range(col_count):
        col_windows = [i for i in range(len(windows))][
            row_count * col : row_count * (col + 1)
        ]
        win_height = int((term.height - 2) / len(col_windows))
        for win in col_windows:
            windows[win].x = win_width * col + 1
            windows[win].y = win_height * col_windows.index(win) + 1
            windows[win].w = win_width
            windows[win].h = win_height


def main_loop(term, screen):
    sighook = SignalHook()
    selected_window = 0
    windows[selected_window].selected = True
    windows[selected_window].draw_frame()
    while not sighook.exit:
        force = False
        key_code = screen.getch()

        while key_code != curses.ERR:
            force = force or (key_code != curses.ERR)
            if key_code in [ord("q"), ord("Q")]:
                return
            elif key_code == curses.KEY_RESIZE:
                draw_app(term)
                calculate_windows(term)
                for window in windows:
                    window.select_lines()
            elif key_code == 9:  # TAB
                windows[selected_window].selected = False
                selected_window += 1
                if selected_window >= len(windows):
                    selected_window = 0
                windows[selected_window].selected = True
            elif key_code == curses.KEY_UP:  # also scroll up
                windows[selected_window].scroll_up()
            elif key_code == curses.KEY_PPAGE:  # PGUP
                windows[selected_window].page_up()
            elif key_code == curses.KEY_DOWN:  # also scroll down
                windows[selected_window].scroll_down()
            elif key_code == curses.KEY_NPAGE:  # PGDN
                windows[selected_window].page_down()
            elif key_code == ord(" "):
                windows[selected_window].scroll_end()
            key_code = screen.getch()

        draw_clock(term)
        for window in windows:
            window.refresh(force)
        tprint(term)
        time.sleep(LOOP_MS / 1000)


def logview():
    term = blessings.Terminal()
    if not term.is_a_tty:
        print("logview output cannot be piped, it is for display only")
    elif term.number_of_colors < 16:
        print("logview requires a terminal that supports a minimum of 16 colours")
    else:
        global config
        config = parse_args()
        print(f"\x1b]2;{APPLICATION_TITLE}\x07", end="")
        colors.extend(COLORS[term.number_of_colors])
        for filename in config.file:
            filepath = os.path.abspath(os.path.join(config.dir, filename))
            if os.access(filepath, os.R_OK, effective_ids=True):
                windows.append(Window(filepath))
            elif os.access(filepath, os.F_OK, effective_ids=True):
                print(f"File '{filepath}' is not readable")
            else:
                print(f"File '{filepath}' does not exist")
            if windows[-1].fd is None:
                windows.pop(len(windows) - 1)

        if windows:
            try:
                screen = curses.initscr()
                curses.noecho()
                curses.cbreak()
                screen.keypad(True)
                screen.nodelay(True)
                screen.getch()

                print(
                    term.enter_fullscreen
                    + term.hide_cursor
                    + term.color(colors[APP_FG])
                    + term.on_color(colors[APP_BG])
                    + term.clear
                )
                draw_app(term)
                calculate_windows(term)
                for window in windows:
                    window.start(term)
                with futures.ThreadPoolExecutor() as pool:
                    threads = {pool.submit(window.load): window for window in windows}
                    for future in futures.as_completed(threads):
                        threads[future].refresh(True)
                main_loop(term, screen)
            except Exception as err:
                raise err
            finally:
                tprint(term, term.exit_fullscreen + term.normal_cursor)
                curses.nocbreak()
                screen.keypad(False)
                curses.echo()
                curses.endwin()
                print(*log, sep="\n")
            exit(0)
    exit(1)


if __name__ == "__main__":
    logview()

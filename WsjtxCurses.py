# -*- coding: utf-8 -*-
import curses
import time
import thread
import locale

class WsjtxCurses:
    def __init__(self):
        self.stdscr = curses.initscr()
        # don't display keys
        curses.noecho()
        # don't need key + enter
        curses.cbreak()
        # remove cursor
        curses.curs_set(0)
        self.stdscr.keypad(1)

        #stdscr.border(0)
        self.height, self.width = self.stdscr.getmaxyx()

        self.header = self.stdscr.subwin(3, self.width, 0, 0)
        self.header.box()

        self.main_win = self.stdscr.subwin(20, self.width-2, 3, 1)
        self.main_win.scrollok(True)

        self.setup_colours()

        # self.main()

    def setup_colours(self):
        curses.start_color()
        # 0 - NOT_WORKED
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        # 1 - WORKED_COUNTRY_AND_STATION
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # 2 - WORKED_COUNTRY_NOT_STATION
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        # 3 - WORKED_COUNTRY_DIFF_BAND
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def add_to_window(self):
        global thread_flag
        for x in range(1,30):
            self.add_main_window("this is a bit of text ({})\n".format(x))
            self.update_heartbeat("10:11:{:0>2}".format(str(x)))
            time.sleep(0.5)
            if not self.thread_flag:
                break

    def get_band(self, freq):
        bands = {"70": "4m",
                    "50": "6m",
                    "28": "10m",
                    "24": "12m",
                    "21": "15m",
                    "18": "17m",
                    "14": "20m",
                    "10": "30m",
                    "7" : "40m",
                    "3" : "80m"
                }
        f = str(freq/1000/1000).split(".")
        return bands[f[0]]

    def set_banner(self, freq, mode, tx):
        self.header.addstr(1, 2, "Freq: {:,}".format(freq))
        self.header.addstr(1, 20, self.get_band(freq))
        self.header.addstr(1, 24, "TX:{}".format(str(tx).ljust(5)))
        self.header.addstr(1, 34, "TxMode:{}".format(mode.ljust(6)))
        self.header.refresh()
        self.stdscr.refresh()

    def update_heartbeat(self, ts):
        # self.header.addstr(1, self.width-15, "{} {}".format(u"\u2665".encode('utf-8'), ts))
        self.header.addstr(1, self.width-16, "{} {}".format("Ping:", ts))
        self.header.refresh()
        self.stdscr.refresh()

    def add_cq(self, before, the_text, colour, after):
        self.main_win.addstr("CQ CALLED BY ")
        self.main_win.addstr("{}".format(the_text), curses.color_pair(colour)|curses.A_BOLD)
        self.main_win.addstr(" {}\n".format(after))
        self.main_win.refresh()
        self.stdscr.refresh()

    def add_main_window(self, text):
        self.main_win.addstr("{}\n".format(text))
        self.main_win.refresh()
        self.stdscr.refresh()

    def main(self):
        # self.set_banner("14.076.00", "JT65/JT9", "Tx")
        #
        # self.thread_flag = True
        # thread.start_new_thread(self.add_to_window, ())

        key = ''
        while True:
            key = self.stdscr.getch()
            if key == ord('q'):
                # self.thread_flag = False
                # break
                pass
            elif key == curses.KEY_DOWN:
                # scroll down ?
                self.main_win.scroll(-1)
                pass
            elif key == curses.KEY_UP:
                # scroll up ?
                self.main_win.scroll(1)
                pass

        self.exit_now()

    def exit_now(self):
        # self.thread_flag = False
        self.stdscr.refresh()

        # end
        curses.nocbreak()
        curses.echo()
        curses.endwin()

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')    # set your locale
    gui = WsjtxCurses()

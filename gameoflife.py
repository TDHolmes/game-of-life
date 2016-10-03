#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import time
import sys
import random


def print_color(string, color, bright=False):
    color_dict = {"black": 0, "red": 1, "green": 2, "yellow": 3,
                  "blue": 4, "magenta": 5, "cyan": 6, "white": 7}
    fmt_str_base = "\x1b[3{}m"
    bright_str = ";1m"
    col = color.strip().lower()
    fmt_str = fmt_str_base.format(color_dict[col])
    if bright:
        fmt_str = fmt_str[:-1] + bright_str
    return fmt_str + string + fmt_str_base.format(color_dict["black"])


class GameOfLife:
    def __init__(self, rows, cols, init_config_file=None):
        """
        Rules:
        1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
        2. Any live cell with two or three live neighbours lives on to the next generation.
        3. Any live cell with more than three live neighbours dies, as if by over-population.
        4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        """
        self.rows = rows
        self.cols = cols
        self.game_arr = [[0 for y in range(cols + 2)] for x in range(rows + 2)]
        self.initialize_board(init_config_file)

    def initialize_board(self, init_config_file):
        if init_config_file is None:
            # random initialization
            for y in range(self.cols + 2):
                for x in range(self.rows + 2):
                    # make sure we're inside the printable play area. There is an invisable
                    # ring around the play area that is always unpopulated
                    in_bounds = (x != 0 and y != 0 and x != self.rows + 1 and y != self.cols + 1)
                    if random.random() > 0.2 and in_bounds:
                        self.game_arr[x][y] = 1
                    else:
                        self.game_arr[x][y] = 0
        else:
            with open(init_config_file, "r") as conf_file:
                configuration = conf_file.read()
            conf_split = configuration.splitlines()
            conf_y = len(conf_split)
            conf_x = len(conf_split[0])
            # initialize based on configuration
            for y in range(self.cols + 2):
                for x in range(self.rows + 2):
                    # make sure we're inside the printable play area. There is an invisable
                    # ring around the play area that is always unpopulated
                    in_board_bounds = (x != 0 and y != 0 and x != self.rows + 1 and y != self.cols + 1)
                    in_conf_bounds = (x <= conf_x and y <= conf_y)
                    if in_board_bounds:
                        if in_conf_bounds:
                            if conf_split[y - 1][x - 1] == "1":
                                self.game_arr[x][y] = 1
                            else:
                                self.game_arr[x][y] = 0
                    else:
                        self.game_arr[x][y] = 0

    def print_board(self):
        string = "\n  "
        for y in range(1, self.cols + 1):
            for x in range(1, self.rows + 1):
                if self.game_arr[x][y]:
                    string += print_color("█", "white", True)
                else:
                    string += print_color("█", "black", True)
            string += "\n  "
            sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.write(string)
        sys.stdout.flush()

    def evaluate_board(self):
        neighbour_array = [[0 for y in range(self.cols + 2)] for x in range(self.rows + 2)]
        for y in range(1, self.cols + 1):
            for x in range(1, self.rows + 1):
                # loop through the 9 neighbors and count them
                neighbours = 0
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        if i == 0 and j == 0:
                            pass
                        else:
                            neighbours += self.game_arr[x + i][y + j]
                neighbour_array[x][y] = neighbours
        # loop through the neighbour array and weed out the generations
        for y in range(1, self.cols + 1):
            for x in range(1, self.rows + 1):
                neighbours = neighbour_array[x][y]
                if self.game_arr[x][y] == 1:
                    # cell is alive. Should it die?
                    if neighbours < 2 or neighbours > 3:
                        self.game_arr[x][y] = 0
                else:
                    # cell is dead. Should it regenerate?
                    if neighbours == 3:
                        self.game_arr[x][y] = 1


def main(rows, cols, delay_time=0):
    life = GameOfLife(rows, cols, "./gun.life")
    while True:
        try:
            start_time = time.time()
            life.print_board()
            while time.time() - start_time < delay_time:
                time.sleep(0.005)
            life.evaluate_board()
        except:
            print("\x1B[0m")
            raise ValueError


if __name__ == '__main__':
    main(80, 40)

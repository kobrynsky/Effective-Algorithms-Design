import os
from pandas import *

import numpy
from pathlib import Path

from helpers import parse_int, get_all_ints_from_string, lets_say_its_inf


class Graph:
    number_of_cities = 0
    cost_matrix = [int, int]
    neighbourhood_matrix = [bool, bool]
    best_cycle_cost = int
    all_numbers = []
    absolute_directory = ""
    x_position = int
    y_position = int
    started_parsing_numbers = bool
    file_name = ""

    def __init__(self, filename="", choice=-1):
        self.best_cycle_cost = lets_say_its_inf()
        self.file_name = filename
        self.x_position = 0
        self.y_position = 0
        self.absolute_directory = os.path.dirname(os.path.realpath(__file__)) + "\\matrixes\\"
        if choice == 0:
            self.parse_small_graph(self.absolute_directory, self.file_name)
        if choice == 1:
            self.parse_large_graph(self.absolute_directory, self.file_name)

    def parse_small_graph(self, absolute_directory, file_name):
        absolute_directory = absolute_directory + "small\\" + file_name
        with open(absolute_directory) as file:
            line = file.readline()
            self.number_of_cities = get_all_ints_from_string(line)[0]
            self.all_numbers = get_all_ints_from_string(file.read())
        self.neighbourhood_matrix = numpy.zeros((self.number_of_cities, self.number_of_cities), dtype=bool)
        self.cost_matrix = numpy.zeros((self.number_of_cities, self.number_of_cities), dtype=int)
        self.create_cost_matrix()
        self.set_infinity_on_inaccessible_places()
        self.create_neighbourhood_matrix()

    def parse_large_graph(self, absolute_directory, file_name):
        absolute_directory = absolute_directory + "large\\" + file_name
        with open(absolute_directory) as file:
            line = file.readline()
            while "DIMENSION" not in line:
                line = file.readline()
            self.number_of_cities = get_all_ints_from_string(line)[0]
            while "EDGE_WEIGHT_SECTION" not in line:
                line = file.readline()
            self.all_numbers = get_all_ints_from_string(file.read())
        self.neighbourhood_matrix = numpy.zeros((self.number_of_cities, self.number_of_cities), dtype=bool)
        self.cost_matrix = numpy.zeros((self.number_of_cities, self.number_of_cities), dtype=int)
        self.create_cost_matrix()
        self.set_infinity_on_inaccessible_places()
        self.create_neighbourhood_matrix()

    def set_infinity_on_inaccessible_places(self):
        for x in range(self.number_of_cities):
            self.cost_matrix[x, x] = lets_say_its_inf()

    def try_parse_number_of_cities(self, line_text_array):
        success = False
        for word in line_text_array:
            if "DIMENSION:" in word:
                success = True
            if success:
                number_of_cities = parse_int(word)
                if number_of_cities:
                    return True
        return False

    def parse_numbers_to_matrix(self, line_text_array):
        for word in line_text_array:
            if "EDGE_WEIGHT_SECTION" in word:
                self.started_parsing_numbers = True
            if self.started_parsing_numbers:
                success = parse_int(word)
                if success:
                    self.cost_matrix[self.x_position, self.y_position] = success
                    if self.x_position < self.number_of_cities - 1:
                        self.x_position += 1
                    else:
                        self.x_position = 0
                        self.y_position += 1
            if self.x_position == self.number_of_cities - 1 & self.y_position == self.number_of_cities - 1:
                self.end_parsing_from_file = True

    def create_cost_matrix(self):
        aux = 0
        for x in range(self.number_of_cities):
            for y in range(self.number_of_cities):
                self.cost_matrix[x, y] = self.all_numbers[aux]
                aux += 1

    def create_neighbourhood_matrix(self):
        for x in range(self.number_of_cities):
            for y in range(self.number_of_cities):
                if self.cost_matrix[x, y] != lets_say_its_inf():
                    self.neighbourhood_matrix[x, y] = True
                else:
                    self.neighbourhood_matrix[x, y] = False

    def display_cost_matrix(self):
        print(DataFrame(self.cost_matrix))
        print("\n")

    def display_neighbourhood_matrix(self):
        print(DataFrame(self.neighbourhood_matrix).astype(int))
        print("\n")

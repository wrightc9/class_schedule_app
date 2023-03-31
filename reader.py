#  Title:		Csv reader implementation
#  Purpose:     This class allows the major csv files to be read and processed into a usable format for
#                   the rest of the program.
# 
#  TC:          O(n^3)

import csv
from pathlib import Path

class Reader:
    def __init__(self) -> None:
        # Contains the processed csv data
        self.courseDict = {}
        # Contains the status of validation, and any error message
        self.valid_format = [True, '']

    # Takes in the input file name, and checks to see if there are any clear syntax errors. It then proceeds to 
    # convert the csv data into a dictionary format
    def read(self, file_name):
        # Checking if file exists
        if not Path(file_name).is_file():
            self.valid_format[0] = False
            self.valid_format[1] = 'Incorrect file name, please re-run the program!'
            return
        with open(file_name) as file:
            reader = csv.reader(file, delimiter=',', skipinitialspace=True)
            line = 0
            # Checking to ensure the number of columns is correct
            for row in reader:
                if len(row) != 5:
                    self.valid_format[0] = False
                    self.valid_format[1] = f'Error on line {line + 1}, incorrect number of columns!'
                    return
                if line == 0:
                    line += 1
                # converts the list in the csv to actual lists, and stores course data as a key-value pair,
                # with the first column being the key, and the rest residing in a list as its value
                else:
                    if ']' in row[3] and '[' in row[3]:
                        row[3] = row[3].strip('][').split(', ')
                    else:
                        self.valid_format[0] = False
                        self.valid_format[1] = f"Error on line {line + 1}, fourth column is not a list!"
                        return

                    if ']' in row[4] and '[' in row[4]:
                        row[4] = row[4].strip('][').split(', ')
                    else:
                        self.valid_format[0] = False
                        self.valid_format[1] = f"Error on line {line + 1}, fifth column is not a list!"
                        return
                
                    self.courseDict[row[0]] = row[1:]
                    line += 1

        self.validate_line()

    # Used to conduct some more advanced validation, it checks each course to ensure that the proper syntax is being
    # used to represent the alternative pre-reqs, and that the course quarters are valid
    def validate_line(self):
        line = 1
        for course, attributes in self.courseDict.items():
            for alternatives in attributes[2]:
                alternatives_list  = alternatives.split(' | ')
                for c in alternatives_list:
                    if ("|" in c):
                        self.valid_format[0] = False
                        self.valid_format[1] = f'Error on line {line + 1}, incorrect alternative format: use " | "!'
                        return

            for quarter in attributes[3]:
                if quarter == "":
                    self.valid_format[0] = False
                    self.valid_format[1] = f'Error on line {line + 1}, course is not offered!'
                    return
                elif int(quarter) < 1 or int(quarter) > 3:
                    self.valid_format[0] = False
                    self.valid_format[1] = f'Error on line {line + 1}, incorrect quarter format: use numbers 1, 2, or 3!'
                    return
                
            line += 1

    # Prints out the dictionary containing the classes
    def print_info(self):
        print(f'Printing the list: {self.courseDict}')

    # Clears any validation errors
    def clear_error(self):
        self.valid_format = [True, '']

    # Removes all data from the reader, and clear validation errors
    def clear(self):
        self.clear_error()
        self.courseDict.clear()
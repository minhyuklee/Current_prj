import csv
import numpy as np
from glob import glob

# Remove axis according to 'valid_axis' list
def remove_axis(python_path="none"):
    result, valid_axis = [], [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18, 22, 23, 24, 43, 44, 45, 46, 47, 48]

    with open(python_path) as f:
        for index, line in enumerate(csv.reader(f)):
            result.append(line) if index + 1 in valid_axis else None
    
    with open('D:\\MinHyuk\\Hand Sign Recognition\\2021_SLT_prj\\DATA\\test\\test.csv', 'w', newline='') as f:
        for line in result:
            csv.writer(f).writerow(line)

# Make a interpolation
def interpolate(python_path="none", matlab_path="none"):
    PYTHON_DATA_LENGTH = len(list(csv.reader(open(python_path)))[0])
    MATLAB_DATA_LENGTH = len(list(csv.reader(open(matlab_path)))[0])
    ratio = (MATLAB_DATA_LENGTH - 1) / (PYTHON_DATA_LENGTH - 1)
    interpolate_result = []

    # Procedure check the element's value is '-10' in python file and interpolate it using mean value
    with open(python_path) as f:
        for line in csv.reader(f):
            float_line = list(map(float, line)) # To handle, convert string list "line" to "float" list
            invalid_loc = [i for i, x in enumerate(float_line) if x == -10] # Extract the location of element which is value -10
            
            # Interpolate "p" point with "p1" and "p2" point, where the order is p1 << p << p2
            for p_index in invalid_loc:
#                 p1_index = p_index - 1
                p1_index = max([index for index, value in enumerate(float_line) if value != -10 and index < p_index])
                p2_index = min([index for index, value in enumerate(float_line) if value != -10 and index > p_index])
                p_value = float_line[p1_index] + (float_line[p2_index] - float_line[p1_index]) * (p_index - p1_index) / (p2_index - p1_index) # Linear interpolation method (https://en.wikipedia.org/wiki/Linear_interpolation)
                float_line[p_index] = round(p_value, 2)

            interpolate_result.append(float_line)

    final_result = [[0 for i in range(MATLAB_DATA_LENGTH)] for j in range(len(interpolate_result))] # Make 2D array, same column with 'MATLAB' & same row with 'PYTHON'
    valid_loc = []

    # Filling the value in 'final_result' list with some stride
    for row_index, row in enumerate(interpolate_result):
        count = 0

        # The values of "interpolation_result" are inserted in final result and that locations are inserted in valid_loc
        while count * ratio < MATLAB_DATA_LENGTH:
            valid_loc.append(round(count * ratio)) if row_index == 0 else None
            final_result[row_index][round(count * ratio)] = row[count]
            count += 1
    
    # Interpolate the element of 'final_result' list which value is 0
    for row_index, row in enumerate(final_result):
        # p1, p2 points are valid pixel and the pixels between them are invalid
        # Process interpolation invalid pixel using p1 and p2 value
        for x in range(len(valid_loc) - 1):
            p1_index, p2_index = valid_loc[x], valid_loc[x + 1]
            p1_value, p2_value = final_result[row_index][p1_index], final_result[row_index][p2_index]
            dis = (p2_value - p1_value) / (p2_index - p1_index)

            for i in range(p1_index + 1, p2_index):
                final_result[row_index][i] = round(final_result[row_index][i - 1] + dis, 4)

    with open("D:\\MinHyuk\\Hand Sign Recognition\\2021_SLT_prj\\DATA\\test\\test-interpolate.csv", "w", newline='') as t:
        for line in final_result:
            csv.writer(t).writerow(line)

remove_axis('D:\\MinHyuk\\Hand Sign Recognition\\2021_SLT_prj\\DATA\\test\\[Python]PJH-sentence1-2021090515476-1-sample1.csv')
interpolate('D:\\MinHyuk\\Hand Sign Recognition\\2021_SLT_prj\\DATA\\test\\test.csv', 'D:\\MinHyuk\\Hand Sign Recognition\\2021_SLT_prj\\DATA\\test\\[MATLAB]PJH-sentence1-2021090515476-1-sample1.csv')
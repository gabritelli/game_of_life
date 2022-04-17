#import libraries
import numpy as np
import matplotlib

#get input file from "input" folder and validate format
def get_input():
    with open('input/input_file.txt', 'r+') as input:
        input = input.read().split('\n')
        n_gen = input[0]
        shape = input[1]
        matrix = input[2:]
        return n_gen, shape, matrix

#structure validation
def check_structure(shape, matrix):
    check = True
    if int(shape.split(' ')[0]) == len(matrix):
        for elem in matrix:
            if len(elem) != int(shape.split(' ')[1]):
                check = False
        return check
    else:
        return False

#return a binary matrix equal to input matrix
def get_binary_matrix(shape, matrix):
    if check_structure(shape, matrix):
        binary_matrix = np.zeros((int(shape.split(' ')[0]), int(shape.split(' ')[1])))
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x] == '*':
                    binary_matrix[y][x] = 1
        return binary_matrix

def count_live_neighbours(y,x,matrix):
    count = 0
    for i in [-1,+1]:
        try:
            if matrix[y+i][x] == 1:
                count += 1
            if matrix[y][x+i] == 1:
                count += 1
            if matrix[y-i][x+i] == 1:
                count += 1
            if matrix[y+i][x+1] == 1:
                count += 1
        except:
            continue
    return count

#Any live cell with fewer than two live neighbours dies.
def check_rule_1(y,x,matrix):
    count = count_live_neighbours(y,x,matrix)
    return True if count < 2 else False

#Any live cell with two or three live neighbours lives on to the next generation.
def check_rule_2(y,x,matrix):
    count = count_live_neighbours(y,x,matrix)
    return True if (count == 2 or count == 3) else False

#Any live cell with more than three live neighbours dies.
def check_rule_3(y,x,matrix):
    count = count_live_neighbours(y,x,matrix)
    return True if count > 3 else False

#Any dead cell with exactly three live neighbours becomes a live cell.
def check_rule_4(y,x,matrix):
    count = count_live_neighbours(y,x,matrix)
    return True if count == 3 else False

def get_new_gen_matrix(matrix):
    new_gen_matrix = np.zeros(matrix.shape)
    for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x] == 1:
                    if check_rule_1(y,x,matrix) == True:
                        new_gen_matrix[y][x] = 0
                    if check_rule_2(y,x,matrix) == True:
                        new_gen_matrix[y][x] = 1
                    if check_rule_3(y,x,matrix) == True:
                        new_gen_matrix[y][x] = 0
                else:
                    if check_rule_4(y,x,matrix) == True:
                        new_gen_matrix[y][x] = 1
    return new_gen_matrix



n_gen, shape, matrix = get_input()
matrix = get_binary_matrix(shape, matrix)
new_gen_matrix = get_new_gen_matrix(matrix)

output = 'Generation ' + str(int(n_gen.split(' ')[1].replace(':',''))+1) + '\n' + str(shape) + '\n'
for row in range(len(new_gen_matrix)):
    for col in range(len(new_gen_matrix[row])):
        if new_gen_matrix[row][col] == 0:
            output += '.'
        else:
            output += '*'
    output += '\n'

text_file = open("output/output_file.txt", "w+")
text_file.write(output)
text_file.close()


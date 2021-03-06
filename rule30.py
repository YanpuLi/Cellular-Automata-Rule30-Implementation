'''
To run this script, first entering the directory where you storing this script

python rule30.py

Rule30Class is a implementation of Cellular Automata Rule30

The initial status of a Rule30Class instance will generate first_row, rowLength,
columnLength, and a matrix(containing the first_row)

new_row function is used for generating new_row by inputing a previous row, also return
pattern_map, in order to generate the pattern_map
(suppose an initial pattern_map is an empty dictionary), I transferred the 6-element submatrix
into decimal for representing, use this as key, and its location as value.
for example:  100010    is a submatrix, suppose the coordinates of the 5th element is (1,1)
            so this submatrix = 1*2**5 + 1*2**1 = 34,
            pattern_map = {34: [(1,1)]}

show_matrix function: display the matrix with only 0, 1 (no '[', ']', or others)

get_pattern_occurrencies function: suppose pattern_k is a string, like this: '1-1-0/1-0-0'
first change it to decimal, then doing comparison in pattern_map
'''
import numpy as np

input_data = np.genfromtxt('./first_row.csv', delimiter=',', dtype=int)

class Rule30Class(object):

    def __init__(self, first_row, rowLength):
        ''' initiate the matrix with firstRow, rowLength is 100, including the 1st row'''
        self.first_row = first_row
        self.rowLength = rowLength
        self.colLength = len(first_row)
        self.matrix = first_row

    def new_row(self, object, prev_row, pattern_map):
        state = {"111": 0, "110": 0, "101": 0, "000": 0,
                 "100": 1, "011": 1, "010": 1, "001": 1}
        row = [0]
        list1 = []
        '''
        from the second to second last element in the new_row,
        tracking its pattern (A[i-1][j-1], A[i][j-1], A[i+1][j-1]) to determine this one,
        num1 & num2 is used for calculating the decimal
        '''
        for j in range(1,len(prev_row)-1):
            pattern = str(prev_row[j-1]) +str(prev_row[j]) +str(prev_row[j+1])
            row.append(state[pattern])
            num1 = int(pattern[0])*2**5 + int(pattern[1])*2**4 + int(pattern[2])*2**3 + state[pattern]*2**1
            list1.append(num1)

        '''generating the boundaries for each row'''
        row[0] = row[len(prev_row)-2]
        row.append(row[1])

        for z in range(len(list1)):
                if z+2 < len(row):
                    num2 = list1[z] + row[z]*2**2 + row[z+2]*2**0

                if num2 in pattern_map.keys():
                    pattern_map[num2].append((z+1, self.matrix.size/self.colLength))
                else:
                    pattern_map[num2] = [(z+1, self.matrix.size/self.colLength)]

        '''append new row to existing matrix'''
        self.matrix = np.vstack((self.matrix,row))
        return row, pattern_map

    def show_matrix(self):
        print "The result is:"
        result = ''
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                result = result + str(self.matrix[i][j])
        print result

    def get_pattern_occurrencies(self,pattern_k, pattern_map):
        '''
            suppose pattern_k is a string, format like this '1-1-0/1-0-0'
        '''
        coordinates = []
        part1 = pattern_k.split('/')[0]
        part2 = pattern_k.split('/')[1]
        num_k = int(part1.split('-')[0])*2**5+int(part1.split('-')[1])*2**4+\
                int(part1.split('-')[2])*2**3+int(part2.split('-')[0])*2**2+int(part2.split('-')[1])*2**1+\
                int(part2.split('-')[2])*2**0
        if num_k in pattern_map.keys():
            coordinates.append(pattern_map[num_k])
        print coordinates

if __name__ == "__main__":

    instance_of_rule30 = Rule30Class(input_data, 100)
    pattern_map = {}

    '''
        call new_row() 99 times to generate the new matrix
    '''
    for i in range(instance_of_rule30.rowLength-1):
        if i == 0:
            prev = instance_of_rule30.matrix
        else:
            row_index = instance_of_rule30.matrix.shape[0]
            prev = instance_of_rule30.matrix[row_index-1]

        instance_of_rule30.new_row(instance_of_rule30, prev, pattern_map)

    instance_of_rule30.show_matrix()
    #print instance_of_rule30.matrix
    pattern_1 = '1-1-0/1-0-0'
    pattern_2 = '1-1-0/1-0-1'
    pattern_3 = '1-1-0/1-1-0'
    print "After comparison, the result is:"
    instance_of_rule30.get_pattern_occurrencies(pattern_1, pattern_map)
    instance_of_rule30.get_pattern_occurrencies(pattern_2, pattern_map)
    instance_of_rule30.get_pattern_occurrencies(pattern_3, pattern_map)
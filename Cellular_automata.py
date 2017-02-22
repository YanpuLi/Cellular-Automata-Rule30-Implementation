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
        '''
            state: representing Rule30, using temp_row to store every new row, then append to matrix
            suppose the initialized status of a pattern_map is a empty dictionary
        '''
        state = {"111": 0, "110": 0, "101": 0, "000": 0,
                 "100": 1, "011": 1, "010": 1, "001": 1}
        '''
            using pattern_map to store the location of each 6-elements, also translate these 6 elements into decimal,
            using the decimal as key, location as value
            for example:  100010    is a submatrix, suppose the coordinates of the 5th element is (1,1)                 
            so this submatrix = 1*2**5 + 1*2**1 = 34,
            pattern_map = {34: [(1,1)]}
        '''
        
        for i in range(1, object.rowLength):
            temp_row = [0]
            list1 = []
            for j in range(1,object.colLength-1):            
                if i == 1:
                    pattern = str(object.matrix[j-1]) +str(object.matrix[j]) +str(object.matrix[j+1])  
                    
                else:
                    pattern = str(object.matrix[i-1][j-1]) +str(object.matrix[i-1][j]) +str(object.matrix[i-1][j+1])
                    
                temp_row.append(state[pattern])
                num1 = int(pattern[0])*2**5 + int(pattern[1])*2**4 + int(pattern[2])*2**3 + state[pattern]*2**1
                list1.append(num1)
            '''generating the boundaries for each row'''
            
            temp_row[0] = temp_row[object.colLength-2]
            temp_row.append(temp_row[1])
            for z in range(len(list1)):
                if z+2 < len(temp_row):
                    num2 = list1[z] + temp_row[z]*2**2 + temp_row[z+2]*2**0
                    
                if num2 in pattern_map.keys():
                    pattern_map[num2].append((z+1, i))
                else:
                    pattern_map[num2] = [(z+1, i)]
            '''append new row to existing matrix'''
            object.matrix = np.vstack((object.matrix,temp_row))
        return pattern_map
            
    def show_matrix(self):
        print "The result is:"
        print self.matrix
        
            
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
    pattern_map = instance_of_rule30.new_row(instance_of_rule30,instance_of_rule30.first_row, pattern_map)
    
    instance_of_rule30.show_matrix()
    pattern_1 = '1-1-0/1-0-0' 
    pattern_2 = '1-1-0/1-0-1'
    pattern_3 = '1-1-1/1-1-0'
    print "After comparison, the result is:"
    instance_of_rule30.get_pattern_occurrencies(pattern_1, pattern_map)
    instance_of_rule30.get_pattern_occurrencies(pattern_2, pattern_map)
    instance_of_rule30.get_pattern_occurrencies(pattern_3, pattern_map)
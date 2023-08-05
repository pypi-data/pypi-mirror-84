import numpy as np

class Matrix:
    
    def __init__(self, r = 2, c = 2):
        
        self.rows = r
        self.cols = c
        self.data = np.array([[0 for x in range (c)] for y in range(r)]).reshape(r, c)
        self.det = 0
        
    def create(self):
        
        print('Matrix dim {}x{}, introduce {} elements'.format(self.rows,self.cols,self.rows*self.cols))
        
        self.data = np.array([[int(input()) for x in range (self.cols)] for y in range(self.rows)]).reshape(self.rows, self.cols)
        
        return self.data
    
    def __add__(self, other):
        
        #Create a new matrix
        result = Matrix(self.rows, self.cols)

        #Check if the other object is of type Matrix
        if isinstance (other, Matrix):
            
            #Add the corresponding element of 1 matrices to another
            for i in range(self.rows): 
                for j in range(self.cols):
                    result.data[i][j] = self.data[i][j] + other.data[i][j]

        #If the other object is a scaler
        elif isinstance (other, (int, float)):
        #Add that constant to every element of A
            for i in range(self.rows):
                for j in range(self.cols):
                    result.data[i][j] = self.data[i][j] + other
        
        return result
    
    def __mul__(self, other):
        
        #Create a new matrix
        result = Matrix(self.rows, self.cols)

        #Check if the other object is of type Matrix
        if isinstance (other, Matrix):
        
            #Add the corresponding element of 1 matrices to another
            for i in range(self.rows):
                # iterate through columns of Y
                for j in range(self.cols):
                    # iterate through rows of Y
                    for k in range(self.cols):
                        result.data[i][j] += self.data[i][k] * other.data[k][j]

        #If the other object is a scaler
        elif isinstance (other, (int, float)):
        #Add that constant to every element of A
            for i in range(self.rows):
                for j in range(self.cols):
                    result.data[i][j] = self.data[i][j] * other

        return result
    
    def determinant(self):
        
        self.det = np.linalg.det(self.data)
        
        return self.det
    
    def __repr__(self):
        
        return "{}".format(self.data)
import random


class Matrix:
    def __init__(self, lines, columns):
        self.lines = lines
        self.columns = columns
        self.matrix = self.matrix_construction()
        self.tr_matrix = self.matrix_transposition()

    def matrix_construction(self):
        matrix = [[random.randint(1, 10) for j in range(self.lines)] for i in range(self.columns)]
        return matrix

    def multiplying_matrix_number(self, number):
        matrix = [row[:] for row in self.matrix.copy()]
        for i in range(self.lines):
            for j in range(self.columns):
                matrix[i][j] = matrix[i][j] * number
        return matrix

    def matrix_addition(self, matrix_2):
        matrix_addited = [row[:] for row in self.matrix.copy()]
        if len(matrix_addited) == len(matrix_2) and len(matrix_addited[0]) == len(matrix_2[0]):
            for i in range(len(matrix_addited)):
                for j in range(len(matrix_addited[0])):
                    matrix_addited[i][j] += matrix_2[i][j]
            return matrix_addited

    def matrix_subtraction(self, matrix_2):
        matrix_subtracted = [row[:] for row in self.matrix.copy()]
        if len(matrix_subtracted) == len(matrix_2) and len(matrix_subtracted[0]) == len(matrix_2[0]):
            for i in range(len(matrix_subtracted)):
                for j in range(len(matrix_subtracted[0])):
                    matrix_subtracted[i][j] -= matrix_2[i][j]
            return matrix_subtracted

    def matrix_transposition(self):
        matrix = [row[:] for row in self.matrix.copy()]
        transposed_matrix = [[0 for j in range(self.columns)] for i in range(self.lines)]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                transposed_matrix[j][i] = matrix[i][j]
        return transposed_matrix

    def matrix_multiplication(self, matrix_2):
        matrix_1 = [row[:] for row in self.matrix.copy()]
        matrix_2 = [row[:] for row in matrix_2]
        empty_matrix = [[0 for j in range(len(matrix_2[0]))] for i in range(self.lines)]
        if len(matrix_1[0]) == len(matrix_2):
            for i in range(len(matrix_1)):
                a = 0
                for j in range(len(matrix_2[0])):
                    for n in range(len(matrix_2)):
                        a += matrix_1[i][n] * matrix_2[n][j]

                    empty_matrix[i][j] = a
                    a = 0

            return empty_matrix


def print_object_matrix(matrix):
    for row in matrix.matrix:
        for x in row:
            print("{:4d}".format(x), end="")
        print()


def print_matrix(matrix):
    for row in matrix:
        for x in row:
            print("{:4d}".format(x), end="")
        print()


a1 = Matrix(3, 3)
print_object_matrix(a1)
print()
print()
a2 = Matrix(3, 3)
print_object_matrix(a2)
print()
# # print_object_matrix(a2)
# # print()
# print_matrix(a1.tr_matrix)
print_matrix(a1.matrix_multiplication(a2.matrix))
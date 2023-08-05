class Matrix:
    def __init__(self, n, start_point, end_point, walls):
        self.matrix = ["0" for i in range(n*n)]
        self.start = start_point
        self.end = end_point
        self.current_row = start_point[0]
        self.current_column = start_point[1]
        self.walls = walls
        self.path_found = False
        self.size = n
        self.reference = []
        for i in range(int(self.size)):
            row = []
            for j in range(int(self.size)):
                row.append(self.matrix[i])
            self.reference.append(row)
        self.reference[self.start[0]][self.start[1]] = "*"
        self.reference[self.end[0]][self.end[1]] = "#"
        for wall in self.walls:
            row = wall[0]
            column = wall[1]
            self.reference[row][column] = "|"

    def get_element(self, row, column):
        return self.reference[row][column]

    def get_matrix(self):
        return self.reference

    def set_value(self, row, column, value):
        self.reference[row][column] = value
        return self.reference[row][column]

    def up(self):
        try:
            if self.current_row > 0 and self.current_column >= 0:
                if self.reference[self.current_row - 1][self.current_column] == "0":
                    self.reference[self.current_row - 1][self.current_column] = "1"
                    self.current_row -= 1
                    return "Up"
                elif self.reference[self.current_row - 1][self.current_column] == "1":
                    self.current_row -= 1
                    return "Up"
                elif self.reference[self.current_row - 1][self.current_column] == "#":
                    self.path_found = True
                    return "End"
                elif self.reference[self.current_row - 1][self.current_column] == "*":
                    self.current_row -= 1
                    return "Back to Start"
            else:
                return "Out of Matrix"
        except IndexError:
            return "Out of Matrix"

    def down(self):
        try:
            if self.reference[self.current_row + 1][self.current_column] == "0":
                self.reference[self.current_row + 1][self.current_column] = "1"
                self.current_row += 1
                return "Down"
            elif self.reference[self.current_row + 1][self.current_column] == "1":
                self.current_row += 1
                return "Down"
            elif self.reference[self.current_row + 1][self.current_column] == "#":
                self.path_found = True
                return "End"
            elif self.reference[self.current_row + 1][self.current_column] == "*":
                self.current_row += 1
                return "Back to Start"
        except IndexError:
            return "Out of Matrix"

    def right(self):
        try:
            if self.reference[self.current_row][self.current_column + 1] == "0":
                self.reference[self.current_row][self.current_column + 1] = "1"
                self.current_column += 1
                return "Right"
            elif self.reference[self.current_row][self.current_column + 1] == "1":
                self.current_column += 1
                return "Right"
            elif self.reference[self.current_row][self.current_column + 1] == "#":
                self.path_found = True
                return "End"
            elif self.reference[self.current_row][self.current_column + 1] == "*":
                self.current_column += 1
                return "Back to Start"
        except IndexError:
            return "Out of Matrix"

    def left(self):
        try:
            if self.current_row >= 0 and self.current_column > 0:
                if self.reference[self.current_row][self.current_column - 1] == "0":
                    self.reference[self.current_row][self.current_column - 1] = "1"
                    self.current_column -= 1
                    return "Left"
                elif self.reference[self.current_row][self.current_column - 1] == "1":
                    self.current_column -= 1
                    return "Left"
                elif self.reference[self.current_row][self.current_column - 1] == "#":
                    self.path_found = True
                    return "End"
                elif self.reference[self.current_row][self.current_column - 1] == "*":
                    self.current_column -= 1
                    return "Back to Start"
            else:
                return "Out of Matrix"
        except IndexError:
            return "Out of Matrix"

    def clear_paths(self):
        self.current_row = self.start[0]
        self.current_column = self.start[1]
        for i in range(len(self.reference)):
            for j in range(len(self.reference[i])):
                if self.reference[i][j] == "1":
                    self.reference[i][j] = "0"
        for wall in self.walls:
            row = wall[0]
            column = wall[1]
            self.reference[row][column] = "|"
        return self.reference

    def convert_tolist(self):
        listed = []
        for row in self.reference:
            for item in row:
                listed.append(item)
        return listed

    def print_matrix(self):
        for row in self.reference:
            for j in row:
                print(j, end=' ')
            print('\n')


def copyMatrix(matrix, enforceAssertions=True):
    """
    Makes a full copy of a matrix. If enforceAssertions is True, ensures
    that the copied matrix conforms to the style expected of sudokus.
    """

    if enforceAssertions: assert len(matrix) == 9

    out = []
    for row in matrix:
        newRow = row.copy()
        out.append(newRow)

        # Check for conformance of this row, if requested
        if enforceAssertions:
            for elem in row: 
                assert type(elem) is int
                assert elem >= 0
                assert elem <= 9
        if enforceAssertions: assert len(row) == 9

    return out


def countInRow(matrix, row, num):
    """
    Counts the number of instances of num in the specified row
    """
    count = 0
    for column in range(9):
        count += (matrix[row][column] == num)

    return count


def countInColumn(matrix, column, num):
    """
    Counts the number of instances of num in the specified column
    """
    count = 0
    for row in range(9):
        count += (matrix[row][column] == num)

    return count


def countInBox(matrix, row, column, num):
    """
    Counts the number of instances of num in the 3x3 box containing the
    specified cell
    """
    boxRow = row // 3
    boxColumn = column // 3

    count = 0
    for row_i in range(3 * boxRow, 3 * boxRow + 3):
        for col_i in range(3 * boxColumn, 3 * boxColumn + 3):
            count += (matrix[row_i][col_i] == num)

    return count


def cellIsValid(matrix, row, column):
    """
    Determines whether the number in the specified cell is valid. This
    includes checking whether other instances of that number appear in
    the same row, column, or 3x3 box, but does not include checking any
    other number or any other row, column, or 3x3 box.
    """
    num = matrix[row][column]
    if num == 0: return False # 0 is not a valid solution
    if countInRow(matrix, row, num) > 1: return False
    if countInColumn(matrix, column, num) > 1: return False
    if countInBox(matrix, row, column, num) > 1: return False
    return True


def doSolve(matrix, row, column):
    """
    Helper function for solve. Recursively calls to determine whether a
    valid solution is possible for a given input matrix.
    """

    # Base case 1: we've reached the end with a valid solution
    if row > 8: return True

    # Base case 2: if this cell is filled already, then it must be
    # fixed, so move on to the next cell
    if matrix[row][column] != 0:
        return doSolve(matrix, row + (column == 8), (column + 1) % 9)

    for num in range(1, 10): # try all numbers 1 to 9
        matrix[row][column] = num
        if cellIsValid(matrix, row, column):
            if doSolve(matrix, row + (column == 8), (column + 1) % 9):
                return True # Found a valid solution with this number
        
    # If here, didn't find a valid solution with any number
    matrix[row][column] = 0
    return False


def solve(matrix):
    """
    Takes a 2D list of integers (with zeros representing unknown
    numbers) representing the unsolved sudoku and returns a solved
    version. The matrix passed in is not mutated at all. Returns the 
    solved matrix, or None if the matrix is not solveable.
    """

    try:
        matrix = copyMatrix(matrix)
    except AssertionError:
        print("Error: matrix does not conform to sudoku style. Aborting.")
        exit(1)

    # Solve from the start
    foundSolution = doSolve(matrix, 0, 0)

    if foundSolution:
        return matrix
    else:
        return None


def display(matrix, blankCharacter = " "):

    if matrix is None:
        print("Not a valid solution.")
        return
    
    try:
        matrix = copyMatrix(matrix) # Ensures the matrix is valid
    except AssertionError:
        print("Error: cannot display this matrix due to style. Aborting.")

    for i, row in enumerate(matrix):
        if i % 3 == 0:
            print("+-------+-------+-------+")
        for j, num in enumerate(row):
            if j % 3 == 0:
                print("| ", end = "")
            if num == 0:
                print(f"{blankCharacter} ", end = "")
            else:
                print(f"{num} ", end = "")
        print("|")
    print("+-------+-------+-------+")
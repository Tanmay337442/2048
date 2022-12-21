##############################
#       2048 in Python       #
##############################


from random import randint, choice


# create starting square matrix (default length of 4)
def board(n = 4):
    # create square matrix of order n filled with zeroes
    mat = [[0]*n for x in range(n)]
    # add two generated numbers to matrix
    addnum(mat)
    addnum(mat)
    return mat

# add number to matrix
def addnum(mat):
    # list containing zero positions
    zeroes = []
    # generate  number 2 (90% chance) or  number 4 (10% chance)
    n = 2 if randint(1, 10) < 10 else 4
    # iterate over matrix elements
    for x in range(len(mat)):
        # iterates for length of first row since
        # program designed to work for any size of matrices (easier for testing)
        for y in range(len(mat[0])):
            if mat[x][y] == 0:
                # add coordinates of zero to list
                zeroes.append([x, y])
    # set pos to random zero position
    pos = choice(zeroes)
    # set x and y to x and y coordinates of selected zero
    x = pos[0]
    y = pos[1]
    # set matrix element to generated number
    mat[x][y] = n
    return mat


# check game state
def state(mat):
    # iterate over matrix rows
    for row in mat:
        # return win if 2048 in row
        if 2048 in row:
            return 'win'
        # game is not over if zero is in matrix row
        elif 0 in row:
            return 'playing'
    # loop for matrix length - 1 to check next row
    # prevents error when checking elements ahead of current element
    # another solution might be to use exceptions (try/except)
    for x in range(len(mat)-1):
        # loop for matrix length - 1 to prevent error when
        # checking next element
        for y in range(len(mat[0])-1):
            # check if current element is same as next element in row (y+1)
            # or same as the element in same position in next row (x+1)
            if mat[x][y] == mat[x][y+1] or mat[x][y] == mat[x+1][y]:
                return 'playing'
    # check consecutive elements in last row
    for y in range(len(mat[0])-1):
        if mat[len(mat)-1][y] == mat[len(mat)-1][y+1]:
            return 'playing'
    # check consecutive elements in last column
    for x in range(len(mat)-1):
        if mat[x][len(mat)-1] == mat[x+1][len(mat)-1]:
            return 'playing'
    # another possible solution:
    # for x in range(len(mat)):
        # for y in range(len(mat)-1):
            # if mat[x][y] == mat[x][y+1]:
                # return 'playing'
    # for i in range(len(mat)-1):
        # for j in range(len(mat)):
            # if mat[x+1][y] == mat[x][y]:
                # return 'playing'
    return 'loss'
    
# moves in 2048 require the following functions
# to change the matrix

# move nonzero numbers to left
def compact(mat):
    # matrix to contain changed rows
    new = []
    # iterate over matrix rows
    for x in range(len(mat)):
        # add rows to new matrix
        new.append([])
        # iterate over elements
        for y in range(len(mat[0])):
            # add elements to new matrix
            new[x].append(mat[x][y])
    # iterate over matrix rows
    for x in range(len(new)):
        # set accumulator
        y = 1
        # run while loop until y reaches the length of a matrix row
        while y < len(new[0]):
            # check if current element is a number other than zero
            # and previous element is a zero
            if new[x][y] != 0 and new[x][y-1] == 0:
                # delete the zero
                del new[x][y-1]
                # add zero back at end of row
                new[x].append(0)
                # if currently at the second element in a row
                # should go to next element
                # since the previous one is no longer a zero
                if y == 1:
                    y += 1
                # otherwise go to previous element to check for
                # zeroes between two numbers which are not zeroes
                else:
                    y -= 1
            # go to next element
            else:
                y += 1
    return new

# combine matrix elements
def combine(mat):
    pts = 0
    # matrix to contain changed rows
    new = []
    # iterate over matrix rows
    for x in range(len(mat)):
        # add rows to new matrix
        new.append([])
        # iterate over elements
        for y in range(len(mat[0])):
            # add elements to new matrix
            new[x].append(mat[x][y])
    # iterate over matrix elements
    for x in range(len(new)):
        # loop for row length - 1 since checking elements
        # in advance
        for y in range(len(new[0])-1):
            # if current element is not zero and next element
            # is equal to current element
            if new[x][y] != 0 and new[x][y] == new[x][y+1]:
                # the following combines the element on the left:
                # double the current element
                new[x][y] *= 2
                # set next element to zero
                new[x][y+1] = 0
                # add newly created number to points
                pts += new[x][y]
    return new, pts

# flip matrix rows
def flip(mat):
    # matrix to contain changed rows
    new = []
    # iterate over matrix rows
    for x in range(len(mat)):
        # add rows to new matrix
        new.append([])
        # iterate over elements
        for y in range(len(mat[0])):
            # add elements to new matrix in opposite order
            new[x].append(mat[x][len(mat[0])-y-1])
    return new

# transpose matrix
def transpose(mat):
    # matrix to contain changed rows
    new = []
    # iterate over matrix rows
    for x in range(len(mat)):
        # add rows to new matrix
        new.append([])
        # iterate over elements
        for y in range(len(mat[0])):
            # add elements on opposite side of diagonal
            new[x].append(mat[y][x])
    return new

# perform left move on matrix
def left(mat):
    new = compact(mat)
    new = combine(new)
    new = [compact(new[0]), new[1]]
    return new

# perform right move on matrix
def right(mat):
    new = flip(mat)
    new = compact(new)
    new = combine(new)
    new = [compact(new[0]), new[1]]
    new = [flip(new[0]), new[1]]
    return new

# perform up move on matrix
def up(mat):
    new = transpose(mat)
    new = compact(new)
    new = combine(new)
    new = [compact(new[0]), new[1]]
    new = [transpose(new[0]), new[1]]
    return new

# perform down move on matrix
def down(mat):
    new = transpose(mat)
    new = flip(new)
    new = compact(new)
    new = combine(new)
    new = [compact(new[0]), new[1]]
    new = [flip(new[0]), new[1]]
    new = [transpose(new[0]), new[1]]
    return new

# set key : function pairs
keys = {
    "a": left,
    "d": right,
    "w": up,
    "s": down
    }

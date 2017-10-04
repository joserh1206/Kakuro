# Kakuro(Sudoku2) generator and solver
# Board size 5x5-->10x10, 6x8 optimal
# NP-complete

import sys
import itertools
import pprint
import copy
import random
from functools import reduce

__all__ = ["solver", "generator"]

# Maximal squares in a line
MAX_LINE_SQUARES = 9
SR = MAX_LINE_SQUARES + 1
allowedValues = set(range(1, SR))
MAX_SUM = sum(allowedValues)


def getRuns(clue, squares, values):
    return [run for run in itertools.combinations(values, squares) if sum(run) == clue]


def getUnion(s):
    return reduce(set.union, s, set())


def getAllUniqueRuns():
    s = []
    for clue in range(3, MAX_SUM + 1):  # clue must > 2
        for squares in range(2, clue if clue < SR else SR):  # squares must > 1
            runs = getRuns(clue, squares, allowedValues)
            if len(runs) == 1:
                s.append((clue, runs[0]))
    return s


AllUniqueRuns = getAllUniqueRuns()


def getUniqueRunsBySquares(squares):
    return [run for run in AllUniqueRuns if len(run[1]) <= squares]


def getCluesBySquares(squares):
    runs = getUniqueRunsBySquares(squares)
    return [run[0] for run in runs]


def getRandomClueBySquaresValues(squares, values):
    if len(values) > 1:
        start = 1
    elif len(values) == 1:
        start = 2
    else:
        start = 3
    if squares > len(values):
        max = sum(range(1, SR)[-squares:]) - sum(values)
        return random.randint(start, max) + sum(values)
    else:
        return random.randint(1, MAX_LINE_SQUARES) + sum(values)


def getClueBySquaresValues(squares, values):
    if squares >= 2:
        if len(values) == squares:
            return sum(values)
        else:
            runs = getUniqueRunsByExactSquares(squares)
            clues = [run[0] for run in runs if set(run[1]).issuperset(values)]
            if clues == []:
                runs = getTwoRunsByExactSquares(squares)
                clues = [run[0] for run in runs if set(run[1]).issuperset(values)]
            if clues == []:
                if len(values) > 0:
                    return getRandomClueBySquaresValues(squares, values)
                else:
                    return getRandomClueBySquaresValues(squares, set())
            else:
                return clues[0]
    else:
        return -1


def getTwoRunsByExactSquares(squares):
    return [run for run in getAllTwoRuns() if len(run[1]) == squares]


def getUniqueRunsByExactSquares(squares):
    return [run for run in AllUniqueRuns if len(run[1]) == squares]


def getUniqueRunByClueSquares(clue, squares):
    """return either [] or list of exact one element"""
    return [run for run in AllUniqueRuns if run[0] == clue and len(run[1]) == squares]


def getAllCrossRunPairs():
    """return all run pairs that have only one common value
    """
    r = range(len(AllUniqueRuns))
    return [(AllUniqueRuns[i], AllUniqueRuns[j]) for i in r for j in r
            if i < j and len(set(AllUniqueRuns[i][1]) & set(AllUniqueRuns[j][1])) == 1]


def getAllCrossRunsByClueSquares(clue, squares):
    """Suppose (clue, squares) is one of AllUniqueRuns"""
    run0 = getUniqueRunByClueSquares(clue, squares)[:1]
    if run0:
        return [run for run in AllUniqueRuns
                if run != run0 and len(set(run[1]) & set(run0[1])) == 1]
    else:
        return []


def getRandomClue(squares):
    if squares >= 2:
        runs = getUniqueRunsBySquares(squares)
        index = random.randint(0, len(runs) - 1)
        clue, run = runs[index]
        return (clue, len(run), set())
    else:
        return -1


def getAllTwoRuns():
    s = []
    for clue in range(3, MAX_SUM + 1):  # clue must > 2
        for squares in range(2, clue if clue < SR else SR):  # squares must > 1
            runs = getRuns(clue, squares, allowedValues)
            if len(runs) <= 2:
                s.append((clue, runs))
    return s


# Example board
boardRow = 8
boardCol = 6

board = [[-1, {'R': -1, 'B': 23}, {'R': -1, 'B': 41}, -1, {'R': -1, 'B': 29}, {'R': -1, 'B': 13}],
         [{'R': 16, 'B': -1}, 0, 0, {'R': 12, 'B': 32}, 0, 0],
         [{'R': 17, 'B': -1}, 0, 0, 0, 0, 0],
         [{'R': 20, 'B': -1}, 0, 0, 0, 0, -1],
         [-1, {'R': 24, 'B': -1}, 0, 0, 0, {'R': -1, 'B': 17}],
         [-1, {'R': 29, 'B': 16}, 0, 0, 0, 0],
         [{'R': 35, 'B': -1}, 0, 0, 0, 0, 0],
         [{'R': 15, 'B': -1}, 0, 0, {'R': 3, 'B': -1}, 0, 0]]


class Board:
    def __init__(self, br=boardRow, bc=boardCol, board=None):
        self.br = br
        self.bc = bc
        if board is not None:
            self.b = board
        else:
            self.b = Board._getBlankBoard(br, bc)

        self.original = None
        self.clues = []

    def topClue(self, i, j):
        """ for solver"""
        k = i - 1
        while self.b[k][j] != -1 and type(self.b[k][j]) != dict:
            k -= 1
        self.b[i][j] = [self.b[i][j], {'T': (k, j)}]  # must run first
        if self.b[k][j] == -1 or self.b[k][j]['B'] == -1:
            return (-1, -1, set())
        else:
            return self.b[k][j]['B']

    def leftClue(self, i, j):
        """ for solver"""
        k = j - 1
        while self.b[i][k] != -1 and type(self.b[i][k]) != dict:
            k -= 1
        self.b[i][j][1]['L'] = (i, k)  # must run second
        if self.b[i][k] == -1 or self.b[i][k]['R'] == -1:
            return (-1, -1, set())
        return self.b[i][k]['R']

    def getTopClue(self, i, j):
        """ for generator"""
        k = i - 1
        while type(self.b[k][j]) != dict and self.b[k][j] != -1:
            k -= 1
        if self.b[k][j] == -1 or self.b[k][j]['B'] == -1:
            return (-1, -1, set()), -1
        else:
            return self.b[k][j]['B'], k

    def getLeftClue(self, i, j):
        """ for generator"""
        k = j - 1
        while type(self.b[i][k]) != dict and self.b[i][k] != -1:
            k -= 1
        if self.b[i][k] == -1 or self.b[i][k]['R'] == -1:
            return (-1, -1, set()), -1
        return self.b[i][k]['R'], k

    def getSquares(self, i, j):
        if self.b[i][j]['R'] != -1:
            k = j + 1
            while k < self.bc and self.b[i][k] != -1 and type(self.b[i][k]) != dict:
                k += 1
            self.b[i][j]['R'] = (self.b[i][j]['R'], k - j - 1, allowedValues)
        if self.b[i][j]['B'] != -1:
            k = i + 1
            while k < self.br and self.b[k][j] != -1 and type(self.b[k][j]) != dict:
                k += 1
            self.b[i][j]['B'] = (self.b[i][j]['B'], k - i - 1, allowedValues)

    def getUniqueRandomClue(self, squares, values):
        while 1:
            clue = getRandomClueBySquaresValues(squares, values)
            if clue not in self.clues:
                break
        self.clues.append(clue)
        return clue

    def getClue(self, i, j):
        Values = set()
        if self.b[i][j]['R'] == 0:
            k = j + 1
            while k < self.bc and self.b[i][k] != -1 and type(self.b[i][k]) != dict:
                if self.b[i][k] > 0:
                    Values.add(self.b[i][k])
                k += 1
            if k - j - 1 >= 2:
                self.b[i][j]['R'] = (self.getUniqueRandomClue(k - j - 1, Values), k - j - 1, Values)
            else:
                self.b[i][j]['R'] = -1
        if self.b[i][j]['B'] == 0:
            k = i + 1
            while k < self.br and self.b[k][j] != -1 and type(self.b[k][j]) != dict:
                if self.b[k][j] > 0:
                    Values.add(self.b[k][j])
                k += 1
            if k - i - 1 >= 2:
                self.b[i][j]['B'] = (self.getUniqueRandomClue(k - i - 1, Values), k - i - 1, Values)
            else:
                self.b[i][j]['B'] = -1

    def getValueSet0(self, i, j):
        self.b[i][j][0] = getUnion(getRuns(*self.topClue(i, j)))
        self.b[i][j][0] = self.b[i][j][0] & getUnion(getRuns(*self.leftClue(i, j)))

    def getValueSet(self, i, j):
        row, col = self.b[i][j][1]['T']
        self.b[i][j][0] = getUnion(getRuns(*self.b[row][col]['B']))
        row, col = self.b[i][j][1]['L']
        self.b[i][j][0] = self.b[i][j][0] & getUnion(getRuns(*self.b[row][col]['R']))

    def solverpreprocess(self):
        self.original = copy.deepcopy(self.b)
        for i in range(self.br):
            for j in range(self.bc):
                if self.b[i][j] == -1:
                    continue
                elif type(self.b[i][j]) == dict:
                    self.getSquares(i, j)
                elif self.b[i][j] == 0:
                    self.getValueSet0(i, j)

    def getValueSets(self):
        for i in range(self.br):
            for j in range(self.bc):
                if self.b[i][j] == -1:
                    continue
                elif type(self.b[i][j]) == dict:
                    continue
                elif type(self.b[i][j]) == int:
                    continue
                elif type(self.b[i][j]) == list:
                    self.getValueSet(i, j)

    def updateValues(self, i, j):
        value = list(self.b[i][j][0])[0]

        top_i, top_j = self.b[i][j][1]['T']
        clue, squares, allowedValues = self.b[top_i][top_j]['B']
        self.b[top_i][top_j]['B'] = (clue - value, squares - 1, allowedValues - self.b[i][j][0])

        left_i, left_j = self.b[i][j][1]['L']
        clue, squares, allowedValues = self.b[left_i][left_j]['R']
        self.b[left_i][left_j]['R'] = (clue - value, squares - 1, allowedValues - self.b[i][j][0])

        self.b[i][j] = value

    def updateBoard(self):
        for i in range(self.br):
            for j in range(self.bc):
                if self.b[i][j] == -1:
                    continue
                elif type(self.b[i][j]) == dict:
                    continue
                elif type(self.b[i][j]) == int:
                    continue
                elif type(self.b[i][j]) == list:
                    if self.b[i][j][0] == set([]):
                        print
                        i, j, "This kakuro is intrinsically unsolvable."
                    elif len(self.b[i][j][0]) == 1:
                        self.updateValues(i, j)
        self.getValueSets()

    def solver(self):
        """ the solution is stored in self.b as the result if solved successfully """

        self.solverpreprocess()
        # self.b and workcopy are changed dynamically during solving iteration process
        workcopy = copy.deepcopy(self.b)
        while 1:
            self.updateBoard()
            if self.b == workcopy:
                break
            else:
                workcopy = copy.deepcopy(self.b)

        # recover content from original board for printing purpose
        # i.e. pprint.pprint(self.b)
        for i in range(self.br):
            for j in range(self.bc):
                if self.b[i][j] == -1:
                    continue
                elif type(self.b[i][j]) == dict:
                    if self.b[i][j]['B'] != -1:
                        self.b[i][j]['B'] = self.original[i][j]['B']
                    if self.b[i][j]['R'] != -1:
                        self.b[i][j]['R'] = self.original[i][j]['R']
                    self.b[i][j] = (self.b[i][j]['B'], self.b[i][j]['R'])
                elif type(self.b[i][j]) == int:
                    continue
                elif type(self.b[i][j]) == list:
                    self.b[i][j] = list(self.b[i][j][0])

        del workcopy

        if self.solved():
            print ("This kakuro is solved. The unique solution is:")
            self.printBoard()
            return True
        else:
            print ("This kakuro is logically unsolvable. It may or may not have multiple solutions.")
            return False

    @staticmethod
    def _getBlankBoard(br, bc):
        b = []
        for i in range(br):
            b.append([])
            for j in range(bc):
                b[i].append(0)

        b[0][0] = -1
        for i in range(1, br):
            b[i][0] = {'B': -1, 'R': 0}
        for j in range(1, bc):
            b[0][j] = {'B': 0, 'R': -1}

        return b

    def getFirstRandomClues(self):
        """
        return ((16, (7, 9)), (22, (1, 2, 3, 4, 5, 7)))
        return ((7, (1, 2, 4)), (34, (4, 6, 7, 8, 9)))
        """

        runpairs = getAllCrossRunPairs()
        runpairs = [(run1, run2) for (run1, run2) in runpairs
                    if len(run1[1]) < self.br - 1 and len(run2[1]) < self.bc - 1
                    or len(run1[1]) < self.bc - 1 and len(run2[1]) < self.br - 1]
        index = random.randint(0, len(runpairs) - 1)
        run1, run2 = runpairs[index]
        self.clues.append(run1[0])
        self.clues.append(run2[0])
        return runpairs[index]

    @staticmethod
    def generator(br, bc):
        bobj = Board(br, bc)
        b = bobj.b
        clues = bobj.getFirstRandomClues()
        run1, run2 = clues
        if len(run1[1]) < len(run2[1]):
            run1, run2 = run2, run1

        print("Random start runs: ", run1, run2)

        b[1][1] = (set(run1[1]) & set(run2[1])).pop()
        b[0][1]['B'] = (run1[0], len(run1[1]), set())
        b[1][0]['R'] = (run2[0], len(run2[1]), set())

        allowed = set(run1[1])
        allowed.remove(b[1][1])
        allowed = list(allowed)
        for i in range(len(allowed)):
            b[i + 2][1] = allowed[i]
            b[i + 2][0] = {'B': -1, 'R': 0}
        if i + 3 <= br - 1:
            b[i + 3][1] = {'R': getRandomClue(bc - 2), 'B': getRandomClue(br - b[0][1]['B'][1] - 2)}
            b[i + 3][0] = -1
            if i + 3 == br - 2:
                b[i + 4][1] = {'R': getRandomClue(bc - 2), 'B': -1}
                b[i + 4][0] = -1
                b[i + 3][1]['B'] = -1

        allowed = set(run2[1])
        allowed.remove(b[1][1])
        allowed = list(allowed)
        for j in range(len(allowed)):
            b[1][j + 2] = allowed[j]
            b[0][j + 2] = {'R': -1, 'B': 0}
        if j + 3 < bc - 1:
            b[1][j + 3] = {'R': getRandomClue(bc - b[1][0]['R'][1] - 2), 'B': getRandomClue(br - 2)}
            b[0][j + 3] = -1
            if j + 3 == bc - 2:
                b[1][j + 4] = {'R': -1, 'B': getRandomClue(br - 2)}
                b[0][j + 4] = -1
                b[1][j + 3]['B'] = -1

        for i in range(br):
            for j in range(bc):
                if b[i][j] == -1:
                    continue
                elif type(b[i][j]) == dict:
                    if b[i][j]['B'] == -1 and b[i][j]['R'] == -1:
                        b[i][j] == -1
                        continue
                    if type(b[i][j]['B']) == tuple and b[i][j]['B'][1] <= 1:
                        b[i][j]['B'] == -1
                        continue
                    if type(b[i][j]['R']) == tuple and b[i][j]['R'][1] <= 1:
                        b[i][j]['R'] == -1
                        continue
                    if b[i][j]['B'] == 0 or b[i][j]['R'] == 0:
                        bobj.getClue(i, j)
                        continue
                elif type(b[i][j]) == int:
                    (tclue, tsquares, tvalues), tx = bobj.getTopClue(i, j)
                    (lclue, lsquares, lvalues), ly = bobj.getLeftClue(i, j)
                    if tx == -1 and ly == -1:  # singular blank cell between blocks
                        b[i][j] = -1
                        continue
                    elif tx == -1 and ly >= 0:
                        b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                        b[i][j] = {'B': -1, 'R': 0}
                        bobj.getClue(i, j)
                        continue
                    elif ly == -1 and tx >= 0:
                        b[tx][j]['B'] = (sum(lvalues), len(lvalues), lvalues)
                        b[i][j] = {'B': 0, 'R': -1}
                        bobj.getClue(i, j)
                        continue

                    if b[i][j] > 0:
                        b[tx][j]['B'][2].add(b[i][j])
                        b[i][ly]['R'][2].add(b[i][j])
                    elif b[i][j] == 0:
                        valueset = getUnion(getRuns(tclue, tsquares, allowedValues)) - tvalues
                        valueset = valueset & (getUnion(getRuns(lclue, lsquares, allowedValues)) - lvalues)
                        if valueset != set():
                            b[i][j] = valueset.pop()
                            tvalues.add(b[i][j])
                            lvalues.add(b[i][j])
                            b[tx][j]['B'][2].add(b[i][j])
                            b[i][ly]['R'][2].add(b[i][j])
                            if tsquares <= len(tvalues):
                                b[tx][j]['B'] = (sum(tvalues), len(tvalues), tvalues)
                            if lsquares <= len(lvalues):
                                b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                        else:
                            if i == br - 1 and j == bc - 1:
                                b[tx][j]['B'] = (sum(tvalues), len(tvalues), tvalues)
                                b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                                b[i][j] = -1
                            elif i == br - 1 and j <= bc - 3:
                                if len(lvalues) > 1:
                                    b[tx][j]['B'] = (sum(tvalues), len(tvalues), tvalues)
                                    b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                                    b[i][j] = {'B': -1, 'R': 0}
                                    bobj.getClue(i, j)
                                elif len(lvalues) <= 1:
                                    value = random.sample(allowedValues - tvalues - lvalues, 1)[0]
                                    tvalues.add(value)
                                    lvalues.add(value)
                                    b[tx][j]['B'] = (sum(tvalues), len(tvalues), tvalues)
                                    b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                                    b[i][j] = value
                            elif i == br - 1 and j == bc - 2:
                                b[i][j] = -1
                                b[tx][j]['B'] = (sum(tvalues), len(tvalues), tvalues)
                                b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                                b[i][j + 1] = -1
                                (tclue, tsquares, tvalues), tx = bobj.getTopClue(i, j + 1)
                                if tx != -1 and type(b[tx][j + 1]) == dict:
                                    b[tx][j + 1]['B'] = (sum(tvalues), len(tvalues), tvalues)
                            elif i <= br - 3 and j == bc - 1:
                                if tsquares <= len(tvalues) and lsquares <= len(lvalues):
                                    b[tx][j]['B'] = (sum(tvalues), len(tvalues), tvalues)
                                    b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                                    b[i][j] = {'B': getRandomClue(br - 1 - j), 'R': -1}
                                else:
                                    v = (allowedValues - tvalues - lvalues).pop()
                                    tvalues.add(v)
                                    lvalues.add(v)
                                    tclue = tclue if tclue > v + sum(tvalues) else getRandomClueBySquaresValues(
                                        tsquares, tvalues)
                                    b[tx][j]['B'] = (tclue, tsquares, tvalues)
                                    b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                                    b[i][j] = v
                            elif i == br - 2 and j == bc - 1:
                                b[i][j] = -1
                                b[tx][j]['B'] = (sum(tvalues), len(tvalues), tvalues)
                                b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                                b[i + 1][j] = -1
                            elif i == br - 2 and j == bc - 2:
                                b[i][j] = -1
                                b[tx][j]['B'] = (sum(tvalues), len(tvalues), tvalues)
                                b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                                b[i + 1][j] = -1
                                b[i][j + 1] = -1
                                b[i + 1][j + 1] = -1
                                if b[i - 1][j + 1] > 0:
                                    (tclue, tsquares, tvalues), tx = bobj.getTopClue(i - 1, j + 1)
                                    b[tx][j + 1]['B'] = (sum(tvalues), len(tvalues), tvalues)
                            else:
                                if tsquares <= len(tvalues) and lsquares <= len(lvalues):
                                    b[tx][j]['B'] = (sum(tvalues), len(tvalues), tvalues)
                                    b[i][ly]['R'] = (sum(lvalues), len(lvalues), lvalues)
                                    b[i][j] = {'B': 0, 'R': 0}
                                    bobj.getClue(i, j)
                                    if b[i][j]['B'] == -1 and b[i][j]['R'] == -1:
                                        b[i][j] = -1
                                else:
                                    v = (allowedValues - tvalues - lvalues).pop()
                                    tvalues.add(v)
                                    lvalues.add(v)
                                    tclue = tclue if tclue > sum(tvalues) else getRandomClueBySquaresValues(tsquares,
                                                                                                            tvalues)
                                    b[tx][j]['B'] = (tclue, tsquares, tvalues)
                                    lclue = lclue if lclue > sum(lvalues) else getRandomClueBySquaresValues(lsquares,
                                                                                                            lvalues)
                                    b[i][ly]['R'] = (lclue, lsquares, lvalues)
                                    b[i][j] = v

        bobj.generatorpostprocess()

        return bobj

    def generatorpostprocess(self):
        for i in range(self.br):
            for j in range(self.bc):
                if self.b[i][j] == -1:
                    continue
                elif type(self.b[i][j]) == dict:
                    if self.b[i][j]['B'] != -1:
                        self.b[i][j]['B'] = self.b[i][j]['B'][0]
                    if self.b[i][j]['R'] != -1:
                        self.b[i][j]['R'] = self.b[i][j]['R'][0]
                    self.b[i][j] = [self.b[i][j]['B'], self.b[i][j]['R']]
                elif type(self.b[i][j]) == int:
                    continue

        for i in range(self.br):
            for j in range(self.bc):
                if type(self.b[i][j]) == list:
                    if self.b[i][j][0] == 0:
                        self.b[i][j][0] = -1
                    if self.b[i][j][1] == 0:
                        self.b[i][j][1] = -1
                    if self.b[i][j][0] == -1 and self.b[i][j][1] == -1:
                        self.b[i][j] = -1
                    else:
                        self.b[i][j] = (self.b[i][j][0], self.b[i][j][1])

    def getStartBoard(self):
        """Get start board with all clues set and all numbers set to 0"""
        startboard = Board._getBlankBoard(self.br, self.bc)
        for i in range(self.br):
            for j in range(self.bc):
                if self.b[i][j] == -1:
                    startboard[i][j] = -1
                elif type(self.b[i][j]) == tuple:
                    startboard[i][j] = {'B': self.b[i][j][0], 'R': self.b[i][j][1]}
                elif type(self.b[i][j]) == int:
                    startboard[i][j] = 0

        return Board(self.br, self.bc, startboard)

    def solved(self):
        for i in range(self.br):
            for j in range(self.bc):
                if self.b[i][j] == -1:
                    continue
                elif type(self.b[i][j]) == dict:
                    continue
                elif type(self.b[i][j]) == int:
                    continue
                elif type(self.b[i][j]) == list:
                    return False
        return True

    def printBoard(self):
        pprint.pprint(self.b)


def testsolver():
    b = Board(boardRow, boardCol, board)
    b.solver()


def testgenerator():
    while 1:
        b = Board.generator(boardRow, boardCol)

        print
        'Clues: %s' % b.clues
        # b.printBoard()

        print
        'Verifying result...'
        bverify = b.getStartBoard()
        if bverify.solver():
            break


if __name__ == '__main__':
    testgenerator()
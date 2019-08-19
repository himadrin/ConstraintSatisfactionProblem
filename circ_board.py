#Himadri Narasimhamurthy
#Circuit Board CSP
#1/31/19

from CSP import *

#create csp
class CircuitBoard:
    #enter ur pieces simply in piece x and piece y form with character
    def __init__(self, pieces, boardx, boardy):
        self.pieces = pieces
        self.boardx = boardx
        self.boardy = boardy
        self.doms = self.domains()
        self.cons = self.constraints()
        self.solution = None

    #define possible domains
    def domains(self):
        dict = {}

        #for each piece, we initialize a list for the possible positions
        for p in range(len(self.pieces)):
            dict[p] = []

            #board dimensions - piece dimensions
            x = self.boardx - (self.pieces[p][1])
            y = self.boardy - (self.pieces[p][2])
            #print(y)

            #add each board and piece dimension to domain dict
            for i in range(x+1):
                for j in range(y+1):
                    dict[p].append((i, j))

        return dict

    #define constrained dictionary
    def constraints(self):
        constraints = {}

        #constraints are in relation of one piece to another
        for i in range(len(self.pieces)):
            for j in range(len(self.pieces)):

                constraints[(i, j)] = []

                #these are checking pieces
                p1 = self.pieces[i]
                p2 = self.pieces[j]

                #if same piece, continue
                if p1 == p2:
                    continue

                #get possible domains for both pieces
                for d1 in self.doms[i]:
                    for d2 in self.doms[j]:
                        #maximum and minimum of piece width/height and piece location
                        high_x = max((d1[0] + p1[1]), (d2[0] + p2[1]))
                        low_x =  min(d1[0], d2[0])

                        high_y = max((d1[1] + p1[2]), (d2[1] + p2[2]))
                        low_y = min(d1[1], d2[1])

                        #if constraints are within realms of the board dimensions
                        if high_x - low_x >= p1[1] + p2[1] or high_y - low_y >= p1[2] + p2[2]:
                            if high_x<= self.boardx and high_y <= self.boardy:
                                #add the possible locations
                                constraints[(i, j)].append((d1, d2))

        return constraints

    #solve with no heuristics - for test
    def simplesolve(self):
        circ = CSP(self.pieces, self.doms, self.cons)
        self.solution =  circ.backtrack(circ.select_unnassigned, circ.order_values, circ.simple)

    #solve with heuristics - true or false
    def solve_mrv_lcv_mac(self, mrv, lcv, mac):
        circ = CSP(self.pieces, self.doms, self.cons)
        a = circ.select_unnassigned
        b = circ.order_values
        c = circ.simple

        if mrv == True:
            a = circ.mrv
        if lcv == True:
            b = circ.lcv
        if mac == True:
            c = circ.mac_3

        self.solution = circ.backtrack(a, b, c)

    #to test string function - useless
    def create_emptyboard_str(self):
        board_str = ""

        board = [['.' for x in range(self.boardx)] for y in range(self.boardy)]

        for j in range((self.boardy)):
            for i in range(self.boardx):
                board_str += board[j][i]
            board_str += '\n'

        return board_str

    def __str__(self):
        res = ""
        board = [['.' for x in range(self.boardx)] for y in range(self.boardy)]

        #for each solution piece
        for k in self.solution.keys():
            #get it's position and add char value in that list
            for y in range(self.pieces[k][2]):
                for x in range(self.pieces[k][1]):

                    #index from the beginning of res string
                    x_ind = x + self.solution[k][0]
                    y_ind = y + self.solution[k][1]

                    #we print from bottom left up so reverse indexes
                    board[y_ind][x_ind] = self.pieces[k][0]

        #final board printing
        for j in range((self.boardy)):
            for i in range(self.boardx):

                res += board[j][i]
            res += '\n'

        return res


pieces1 = [('a', 3, 2), ('b', 5, 2), ('c', 2, 3), ('e', 7, 1)]

print("\n --------------------------- SOLVE CIRCBOARD WITH NO HEURISTICS OR INFERENCE -------------------------------\n")

cb = CircuitBoard(pieces1, 10, 3)
cb.simplesolve()
print(cb)

print("\n --------------------------- SOLVE CIRCBOARD WITH MRV -------------------------------\n")

cb.solve_mrv_lcv_mac(True, False, False)
print(cb)

print("\n --------------------------- SOLVE CIRCBOARD WITH MRV AND LCV -------------------------------\n")

cb.solve_mrv_lcv_mac(True, True, False)
print(cb)

print("\n --------------------------- SOLVE CIRCBOARD WITH LCV AND MAC-3 INFERENCE -------------------------------\n")

cb.solve_mrv_lcv_mac(False, True, True)
print(cb)
#Himadri Narasimhamurthy
#Australia Color CSP
#1/31/19 - NEED TO REWORK

from CSP import *
from collections import defaultdict

#create csp
class AusMap:
    #take in lists/color/neighbors
    def __init__(self, vars, colors, neighbors):
        self.vars = vars
        self.colors = colors
        self.doms = self.domains(colors)
        self.cons = self.constraints(neighbors)

    #just adds all colors as possible domains
    def domains(self, colors):
        doms = {}

        for v in range(len(self.vars)):
            doms[v] = []

            #add all colors to each var
            for i in range(len(colors)):
                doms[v].append(i)

        return doms

    #generates possible color matches for each pair
    def constraints(self, neighbors):
        #turn our string into a dictionary of neighbors
        neighbor_dict = self.nghbrs_to_dict(neighbors)

        cons = {}

        #constraints are from var to vat
        for i in range(len(self.vars)):
            for j in range(len(self.vars)):
                cons[i,j] = []

                #check along the domains
                for c1 in self.doms[i]:
                    for c2 in self.doms[j]:

                        #if we're checking an impossible color
                        if self.vars[j] in neighbor_dict[self.vars[i]] and c1 == c2:
                                continue

                        #append all possible color combos
                        cons[(i, j)].append((c1, c2))
        return cons

    #helper - whether or not val is in key for neighbor dict
    def in_neighbor_dict(self, dict, val, key):

        for i in dict[key]:
            if i == val:
                return True
        return

    #neighbor string to dictionary
    def nghbrs_to_dict(self, neighbors):

        dict = defaultdict(list)

        #simple string parsing
        parse = []
        for part in neighbors.split(';'):
            parse.append(part.split(':'))

        #add each neighbor/state to each other's neighbor list
        for (st, nghbrs) in parse:
            state = st.strip()
            for neighbor in nghbrs.split():
                dict[state].append(neighbor)
                dict[neighbor].append(state)

        return dict

    #no heuristic testing
    def simplesolve(self):
        aus = CSP(self.vars, self.doms, self.cons)
        return aus.backtrack(aus.select_unnassigned, aus.order_values, aus.simple)

    #just implemented with the mrv heuristic
    def solve_mrv(self):
        aus = CSP(self.vars, self.doms, self.cons)
        return aus.backtrack(aus.mrv, aus.order_values, aus.simple)


australia = AusMap(['South_Australia', 'New_South_Wales', 'Northern_Territory', 'Queensland', 'Western_Australia', 'Victoria', 'Tasmania'], ['G', 'B', 'R'],
                           'South_Australia: Western_Australia Northern_Territory Queensland New_South_Wales Victoria; Northern_Territory: Western_Australia Queensland; New_South_Wales: Queensland Victoria; Tasmania: Victoria')

def print_sol(res):
    for k in res.keys():
        print(str(australia.vars[k]) + " maps to " + str(australia.colors[res[k]]))

#solves with no heuristics or inference
print("\n --------------------------- SOLVE AUSMAP WITH NO HEURISTICS OR INFERENCE -------------------------------\n")

res = australia.simplesolve()
print_sol(res)

print("\n --------------------------- SOLVE WITH MRV -------------------------------\n")

res2 = australia.solve_mrv()
print_sol(res2)
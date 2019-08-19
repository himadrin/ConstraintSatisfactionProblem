#Himadri Narasimhamurthy
#Basic CSP Class
#1/31/19

from queue import deque

class CSP:
    def __init__(self, vars, domain, cons):
        self.vars = vars
        self.domain = domain
        self.cons = cons

        #the domain of things being checked
        self.checking = None

        #whether or not we found solution
        self.failure = False

    #HELPER FUNCTIONS

    #does the assignment of a value to a variable
    def assign(self, var, val, assignments):
        assignments[var] = val

    #removes an assignment - does not change
    def rem_assign(self, var, assignments):
        if var in assignments:
            del assignments[var]

    #helper to return whether or not we are constrained
    def check_constraint(self, var, val, assignment):
        for key in assignment.keys():
            if (val, assignment[key]) not in self.cons[(var, key)] and key != var:
                return False
        return True

    #helper to simply return list if no heuristic selected
    def choose(self, var):
        if self.checking == None:
            return self.domain[var]
        else:
            return self.checking[var]


    #-------------------- BACKTRACKING ----------------------

    #calls the recursive backtrack function with empty assignment
    def backtrack(self, select, order, inference):
        result = self.rec_backtrack({}, select, order, inference)

        #sets failure true if no result found
        if result != None:
            self.failure = False
        else:
            self.failure = True

        return result

    #recursive backtracking function!
    def rec_backtrack(self, assignments, select, order, inference):
        rem = []

        #if we have assigned all variables return
        if len(assignments)== len(self.vars):
            return assignments

        #choose a var and val list based on heuristic
        var = select(assignments)
        val_list = order(var, assignments)

        #go through the values in list
        for val in val_list:

            #if the values are constrained - possible
            if self.check_constraint(var, val, assignments):

                #make the assignment
                self.assign(var, val, assignments)

                #if we are not currently checking anything - make checking dict
                if self.checking is None:
                    self.checking = {}
                    #add all from domains list to checking for the vertex in question
                    for v in range(len(self.vars)):
                        self.checking[v] = list(self.domain[v])

                #create a removed list of all that we have checked
                for checked in self.checking[var]:
                    if checked != val:
                        rem.append((var, checked))

                #add the current to checking list
                self.checking[var] = [val]

                #we add inference before recursing
                if inference(var, assignments, rem):

                    result = self.rec_backtrack(assignments, select, order, inference)

                    if result != None:
                        return result

                #add all removed back to checking til we find goal
                for Key, v in rem:
                    self.checking[Key].append(v)

        #if no goal foumd, we remove all assignments and return none
        self.rem_assign(var, assignments)
        return None

    #VALUE SELECT FUNCTIONS

    #non-heuristic select
    def select_unnassigned(self, assignments):
        for v in range(len(self.vars)):
            if v not in assignments:
                return v

    #should give us variable with fewest remaining values
    def mrv(self, assignments):
        min = 10000000000
        return_v = None

        #count up the remaining values for all v
        for v in range(len(self.vars)):
            if v not in assignments:
                #if we have things in checking - those are remaining
                if self.checking:
                    count = len(self.checking[v])
                    if count<=min:
                        min = count
                        return_v = v
                else:
                    count = 0
                    #else we add from domain
                    for val in self.domain[v]:
                        if self.check_constraint(v, val, assignments):
                            count =+1
                    if count<=min:
                        min = count
                        return_v = v
         #return vertex with lowest count
        return return_v

    #LIST ORDERING FUNCTIONS

    #employs least constraining value principle
    def lcv(self, var, assigments):
        #lists to return and sort
        ordered = []
        remaining = []

        #go through all in domain to count up the constraints
        for v in self.domain[var]:
            c = 0
            for var1 in range(len(self.vars)):
                if var1 not in assigments.keys():
                    #check against each constraint
                    for cons in self.cons[(var, var1)]:

                        #if constrained then increment
                        if v == cons[0]:
                            c = c+1

            # remaining contains values and their constraint counts in tuple
            remaining.append((v, c))

        #sorted from least to greatest constraint count
        remaining.sort(key=lambda count: count[1])

        #add only the value pairs to our list - not counts
        for val in remaining:
            ordered.append(val[0])

        return ordered

    #just simple return list
    def order_values(self, var, assignments):
        return self.choose(var)


    #INFERENCE TECHNIQUE (MAC -3 and no inference)

    #no inference
    def simple(self, var, assignment, rem):
        return True

    #mac_3 inference
    def mac_3(self, var, assignments, rem):

        #create a new queue for inference
        q = deque()

        #go through all vars- checking for impossibles
        for neighbor in range(len(self.vars)):
            if neighbor == var or (len(self.cons[(var, neighbor)])<=0):
                if neighbor not in assignments:
                    q.append((var, neighbor))

        #while q not empty
        while q:
            (a, b) = q.pop()

            #check if we need to remove
            if self.removed(a, b, rem, assignments):
                #if we have removed all from the domain - all impossible
                if len(self.domain[a] == 0):
                    return False

                #check the next variable against the var for whether constrained
                for c in range(len(self.vars)):
                    if c not in assignments and len(self.cons[(var, c)]) > 0:
                        #if so, add to q
                        q.append((c, b))

        return True

    #check if removed from inference
    def removed(self, a, b, rem, assignments):
        revised = False
        con = False

        #for all in domain of a and b
        for d in self.domain[a]:
            for d1 in self.domain[b]:

                #check if constrained
                if (d, d1) in self.cons[(a,b)]:
                    con = True

            #if not constrained - impossible
            if con == False:
                #remove the pait
                rem.append(a, d)
                revised = True

        #for each pair that was removed - prune the domains
        for d1 in rem:
            self.domain[d1[0]].remove(d1[1])

            #if we are not yet checking the removed, we set it as empty
            if d1[0] not in self.checking.keys():
                self.checking[d1[0]] = []

        return revised

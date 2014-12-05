import time
import sys
from project import CSE6140Project

'''Globals
   @INF = Infinity
   @best_cost = Present best cost
   @start_time = For measuring rate
'''

INF = 100000000
best_cost = 0
start_time = time.time()




'''Reducing the Cost Matrix '''

def reduce(size, w, row, col, rowred, colred):
    rvalue = 0
    for i in xrange(size):
        temp = INF
        for j in xrange(size):
            temp = min(temp, w[row[i]][col[j]])
        if temp > 0:
            for j in xrange(size):
                if w[row[i]][col[j]] < INF:
                    w[row[i]][col[j]] -= temp
            rvalue += temp
        rowred[i] = temp
    for j in xrange(size):
        temp = INF
        for i in xrange(size):
            temp = min(temp, w[row[i]][col[j]])
        if temp > 0:
            for i in xrange(size):
                if w[row[i]][col[j]] < INF:
                    w[row[i]][col[j]] -= temp
            rvalue += temp
        colred[j] = temp
    return rvalue

'''Finding the bestedge'''


def bestEdge(size, w, row, col):
    mosti = -INF
    ri = 0
    ci = 0
    for i in xrange(size):
        for j in xrange(size):
            if not w[row[i]][col[j]]:
                minrowwelt = INF
                zeroes = 0
                for k in xrange(size):
                    if not w[row[i]][col[k]]:
                        zeroes += 1
                    else:
                        minrowwelt = min(minrowwelt, w[row[i]][col[k]])
                if zeroes > 1: minrowwelt = 0
                mincolwelt = INF
                zeroes = 0
                for k in xrange(size):
                    if not w[row[k]][col[j]]:
                        zeroes += 1
                    else:
                        mincolwelt = min(mincolwelt, w[row[k]][col[j]])
                if zeroes > 1: mincolwelt = 0
                if minrowwelt + mincolwelt > mosti:
                    mosti = minrowwelt + mincolwelt
                    ri = i
                    ci = j
    return mosti, ri, ci


'''Probing and exploring the nodes'''

def explore(n, w, edges, cost, row, col, best, fwdptr, backptr,filename,cutoff):
    global best_cost
    
    if(float(time.time()-start_time) < float(cutoff)):

        colred = [0 for _ in xrange(n)]
        rowred = [0 for _ in xrange(n)]
        size = n - edges
        cost += reduce(size, w, row, col, rowred, colred)
        if cost < best_cost:
            if edges == n - 2:
                for i in xrange(n): best[i] = fwdptr[i]
                if w[row[0]][col[0]] >= INF:
                    avoid = 0
                else:
                    avoid = 1
                best[row[0]] = col[1 - avoid]
                best[row[1]] = col[avoid]
                best_cost = cost
                
                trace_file = open(filename[:-4]+"_BnB"+"_"+str(cutoff)+".trace",'a')
                trace_file.write(str(time.time()-start_time)+","+str(best_cost)+"\n")
                trace_file.close()

                solution_file = open(filename[:-4]+"_BnB"+"_"+str(cutoff)+".sol",'w')
                solution_file.write(str(best_cost)+"\n")
                for i in range(len(best)):
                    solution_file.write(str(best[i])+",")
            else:
                mostv, rv, cv = bestEdge(size, w, row, col)
                lowerbound = cost + mostv
                fwdptr[row[rv]] = col[cv]
                backptr[col[cv]] = row[rv]
                last = col[cv]
                while fwdptr[last] != INF: last = fwdptr[last]
                first = row[rv]
                while backptr[first] != INF: first = backptr[first]
                colrowval = w[last][first]
                w[last][first] = INF
                newcol = [INF for _ in xrange(size)]
                newrow = [INF for _ in xrange(size)]
                for i in xrange(rv): newrow[i] = row[i]
                for i in xrange(rv, size - 1): newrow[i] = row[i + 1]
                for i in xrange(cv): newcol[i] = col[i]
                for i in xrange(cv, size - 1): newcol[i] = col[i + 1]
                explore(n, w, edges + 1, cost, newrow, newcol, best, fwdptr, backptr,filename,cutoff)
                w[last][first] = colrowval
                backptr[col[cv]] = INF
                fwdptr[row[rv]] = INF
                if lowerbound < best_cost:
                    w[row[rv]][col[cv]] = INF
                    explore(n, w, edges, cost, row, col, best, fwdptr, backptr,filename,cutoff)
                    w[row[rv]][col[cv]] = 0 

        for i in xrange(size):
            for j in xrange(size):
                w[row[i]][col[j]] = w[row[i]][col[j]] + rowred[i] + colred[j]
    else:
        sys.exit("Cutoff Reached")





'' 'Driver function, calls explore repeatedly'''


def tsp(w,filename,cutoff):
    
    global best_cost
    size = len(w)
    col = [i for i in xrange(size)]
    row = [i for i in xrange(size)]
    best = [0 for _ in xrange(size)]
    route = [0 for _ in xrange(size)]
    fwdptr = [INF for _ in xrange(size)]
    backptr = [INF for _ in xrange(size)]
    best_cost = INF

    explore(size, w, 0, 0, row, col, best, fwdptr, backptr,filename,cutoff)

    index = 0
    for i in xrange(size):
        route[i] = index
        index = best[index]
    index = []
    cost = 0

    for i in xrange(size):
        if i != size - 1:
            src = route[i]
            dst = route[i + 1]
        else:
            src = route[i]
            dst = 0
        cost += w[src][dst]
        index.append([src, dst])
    return cost, index


'''Main'''
def BnB(filename,cutoff):
    

    aGraph = CSE6140Project()
    aGraph.load_file(filename)
    trace_file = open(filename[:-4]+"_BnB"+"_"+str(cutoff)+".trace",'w')
    trace_file.close()
    

    m = [[INF for i in range(int(aGraph.parameters['dimensions']))] for j in range(int(aGraph.parameters['dimensions']))]
    
    for i in range(int(aGraph.parameters['dimensions'])):
        for j in range(int(aGraph.parameters['dimensions'])):
            if(i==j):
                m[i][j] = INF
            else:
                for k in range(len(aGraph.m)):
                    if((i==aGraph.m[k][0]-1 and j==aGraph.m[k][1]-1) or(i==aGraph.m[k][1]-1 and j == aGraph.m[k][0]-1)):
                        m[i][j] = aGraph.m[k][2] 
                        m[j][i] = aGraph.m[k][2] 
                        #print m[i][j]

    
    solution_file = open(filename[:-4]+"_BnB"+"_"+str(cutoff)+".sol",'w')

    global start_time 
    start_time = time.time()
    cost, path = tsp(m,filename,cutoff)
    end_time = time.time()
    return path,cost, end_time-start_time
    
if __name__ == "__main__":
    BnB(sys.argv[1],sys.argv[2])

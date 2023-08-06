def read_next_visit(line):
    t, u, a = line.split(',')
    t = float(t)
    a = a.strip()
    return t, u, a
    
def a_not_present(t, u, a, H, LRU, c):
    H[a] = {u}
    LRU[a] = [(t,u)]
    c[a] = 1

def a_present(t, u, a, H, LRU, c):
    if u not in H[a]:
        u_not_present(t, u, a, H, LRU, c)
    else:
        u_present(t, u, a, LRU)

def u_not_present(t, u, a, H, LRU, c):
    H[a].add(u)
    c[a] += 1
    LRU[a].append((t,u))
    
def u_present(t, u, a, LRU):
    for i, (tprime, uprime) in enumerate(LRU[a]):
        if uprime == u:
            del LRU[a][i]
    LRU[a].append((t, u))
    
def evict(t, H, LRU, c, Deltat):
    a_to_remove = []
    for a in LRU.keys():
        while t - LRU[a][0][0] > Deltat:
            to_remove = LRU[a].pop(0)
            H[a].remove(to_remove[1])
            c[a] -= 1
            if len(LRU[a]) == 0:
                a_to_remove.append(a)
                break
    for a in a_to_remove:          
        LRU.pop(a, None)
        H.pop(a, None)
        
def manage_data_structure(t, u, a, H, LRU, c):
    sep = '*'
    cat = a.split(sep)
    for level in range(len(cat)):
        i = '*'.join(cat[:level + 1])
        if i not in H:
            a_not_present(t, u, i, H, LRU, c)
        else:
            a_present(t, u, i, H, LRU, c)
        
def check_and_output(t, u, a, c, z):
    sep = '*'
    cat = a.split(sep)
    counters = []
    anon = False
    for level in reversed(range(len(cat))):
        attr = '*'.join(cat[:level + 1])
        counters.append(c[attr])
        if c['*'.join(cat[:level + 1])] >= z and anon == False:
            output = (t, u, attr)
            anon = True
    f = open('simulation_output.txt', 'a')
    f.write("\t".join(str(x) for x in [t,u,a])+ "\t" + "\t".join(str(x) for x in counters[::-1]) + '\n')
    f.close()
    if anon:
        return output
    else: return None

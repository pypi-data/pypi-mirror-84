def get_cell(lat, lon):
    from pyproj import Transformer
    import numpy as np
    stepsize = np.array([5000, 50000, 100000])
    from_ll_to_mt = Transformer.from_crs('epsg:4326', 'epsg:3857')
    nw = from_ll_to_mt.transform(55, 3.5)
    se = from_ll_to_mt.transform(47.5, 15.5)
    point = from_ll_to_mt.transform(lat, lon)
    distx = point[0] - nw[0]
    disty = nw[1] - point[1]
    cellx = (distx / stepsize).astype(int)
    celly = (disty / stepsize).astype(int)
    maxx = (np.ceil((se[0] - nw[0]) / stepsize)).astype(int)
    cell = celly * maxx + cellx
    return cell.tolist()

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
    for level in reversed(range(len(cat))):
        if c['*'.join(cat[:level + 1])] >= z:
            output = (t, u, a)
            return output
        else: return None

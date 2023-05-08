import itertools
import copy
def generate_strings(N, J):
    # check if N and J are valid
    if N < 0 or J < 0 or J > N:
        return None
    # create a list of '01' repeated N times
    bits = ['01'] * N
    # create an iterator that produces all possible N-bit strings
    product = itertools.product(*bits)

    # filter out the strings that have exactly J ones
    result = ["".join(s) for s in product if s.count('1') == J]
    # return the result as a list

    return result

def xor(a,b):
    if int(a) == int(b):
        return '0'
        #return 0
    else:
        return '1'
        #return 1

def AND(a,b):
    if (a=='1') and (b == '1'):
        return '1'
        #return 1
    return '0'
    #return 0   

def compare(K,X,v,n,J,s,count_needed):
    temp_K=copy.deepcopy(K)
    comp=[0]*n
    leng=len(J)
    for i in range(0, n):
        if X[i] == '1':
            temp_K[v][i]='1'
            count = 0
            for t in range(0, leng):
                At = [AND(temp_K[v][idx] , J[t][idx]) for idx in range(0,n)]
                if At.count('1') >= s:
                    count+=1
            comp[i]=count
            temp_K[v][i]='0'
    # sorted_comp = sorted(comp)
    ch = [0]*n
    index_order = [i for _, i in sorted(zip(comp, range(len(comp))))]#[comp.index(x) for x in sorted_comp]
    for i in range (0,n):
        if index_order[i] < count_needed:
            ch[i]='1'

    return ch

    
def find_K(K,J,t,n,s,k,count_k):
    need = [0]*count_k
    rem = [0]*count_k
    res = [0]*count_k
    for v in range(0, count_k):
        At = [AND(K[v][idx] , J[t][idx]) for idx in range(0, n)]
        need[v] = s - At.count('1')
        rem[v] = k - K[v].count('1')
    for i in range(0,count_k):
        if rem[i] < need[i]:
            res[i] = 99
        else:
            res[i] = need[i]
    index_order = [i for _, i in sorted(zip(res, range(len(res))))]
    return index_order

    
    



def get(m, n, k, j, s):
    # Initialize K and count_k
    K = [['0'] * n]
    #K = [[0] * n]
    #count_k = 1
    ###########################################################
    for a in range(k):
        K[0][a]='1'
    K.append(['0'] * n)
    for a in range(-1,-k,-1):
        K[1][a]='1'
    K.append(['0'] * n)
    idx = n//2 - k//2
    for a in range(idx,idx+k):
        K[2][a]='1'
    ###########################################################
    count_k = 3
    # Generate string J
    J = generate_strings(n, j)

    for t in range(0, len(J)):
        flag = 0
        #print(K)
        for v in range(0, count_k):
            # Calculate At = Kv & Jt
            #At = [K[v][idx] and J[t][idx] for idx in range(0,n)]
            At = [AND(K[v][idx] , J[t][idx]) for idx in range(0,n)]
            if At.count('1') >= s:
                flag = 1# Move to the next combination of J
                break
        if flag == 1:
            continue
        

        order = find_K(K,J,t,n,s,k,count_k)


        for v in order:

            At = [AND(K[v][idx] , J[t][idx]) for idx in range(0, n)]

            count_needed = s - At.count('1')

            if K[v].count('1')<k:

                if (k - K[v].count('1')) >= count_needed:

                    X = [xor(At[idx], J[t][idx]) for idx in range(0, n)]
                    ch = compare(K,X,v,n,J,s,count_needed)


                    for i in range(0, n):
                        if ch[i] == '1':

                            K[v][i] = '1'
                            #K[v][i] = 1
                            count_needed -= 1
                        if count_needed == 0:
                            break
                    break
                else:
                    if v == count_k - 1:
                        # If none of the existing K is enough, create a new one
                        K.append(['0'] * n)
                        #K.append([0] * n)
                        count_k += 1
                        count_needed = s

                        for i in range(0, n):

                            if J[t][i] == '1':
                                K[count_k - 1][i] = '1'
                                #K[count_k - 1][i] = 1
                                count_needed -= 1
                            if count_needed == 0:
                                break
            else:
                if v == count_k - 1:
                    # If none of the existing K is enough, create a new one
                    K.append(['0'] * n)
                    count_k += 1
                    count_needed = s

                    for i in range(0, n):

                        if J[t][i] == '1':
                            K[count_k - 1][i] = '1'
                            count_needed -= 1
                        if count_needed == 0:
                            break
    

    for i in range(0, len(K)):
        cout = K[i].count('1')
        while cout < k:
            for l in range(0, n):
                if K[i][l] == '0':
                    K[i][l] = '1'
                    cout += 1
                    break
    Red_K = []
    [Red_K.append(item) for item in K if item not in Red_K]
    print(len(Red_K))
    return Red_K



if __name__ == '__main__':


    res = get(45,10,6,4,4)
    print(res)



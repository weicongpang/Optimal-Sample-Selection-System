import itertools

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
        return 0
    else:
        return 1

def AND(a,b):
    if(a==1 or a=='1'):
        if (b == 1 or b == '1'):
            return 1
    return 0

def get(m, n, k, j, s):
    # Initialize K and count_k
    K = [[0] * n]
    count_k = 1

    # Generate string J
    J = generate_strings(n, j)

    for t in range(0, len(J)):
        #print(K)
        for v in range(0, count_k):
            # Calculate At = Kv & Jt
            At = [K[v][idx] and J[t][idx] for idx in range(0,n)]
            #At = [AND(K[v][idx] , J[t][idx]) for idx in range(0,n)]
            if At.count('1') >= s:
                # Move to the next combination of J
                break

        for v in range(0, count_k):
            # # Calculate At = Kv & Jt
            At = [K[v][idx] and J[t][idx] for idx in range(0,n)]
            #At = [AND(K[v][idx] , J[t][idx]) for idx in range(0, n)]
            # if At.count(1) >= s:
            #     # Move to the next combination of J
            #     break
            # Calculate X = At XOR Jt
            # X = [xor(At[idx] , J[t][idx]) for idx in range(0,n)]
            count_needed = s - At.count('1')

            if K[v].count(1)<k:
                if (k - K[v].count(1)) >= count_needed:
                    X = [xor(At[idx], J[t][idx]) for idx in range(0, n)]
                    #print(k - K[v].count(1), count_needed)

                    # Add 1s to K to fulfill count_needed
                    for i in range(0, n):
                        if X[i] == 1:
                            #print(i)
                            K[v][i] = 1
                            count_needed -= 1
                        if count_needed == 0:
                            break
                    break
                else:
                    if v == count_k - 1:
                        # If none of the existing K is enough, create a new one
                        K.append([0] * n)
                        count_k += 1
                        count_needed = s

                        for i in range(0, n):

                            if J[t][i] == '1':
                                K[count_k - 1][i] = 1
                                count_needed -= 1
                            if count_needed == 0:
                                break
            else:
                if v == count_k - 1:
                    # If none of the existing K is enough, create a new one
                    K.append([0] * n)
                    count_k += 1
                    count_needed = s

                    for i in range(0, n):

                        if J[t][i] == '1':
                            K[count_k - 1][i] = 1
                            count_needed -= 1
                        if count_needed == 0:
                            break
    valid_K = []
    [valid_K.append(item) for item in K if item not in valid_K]


    #print("valid_K = ",valid_K)
    #print(len(valid_K))
    return valid_K
def show(n,k,valid_k):
    leng = len(valid_k)
    std = ['A', 'B', 'C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    res=[]
    for i in range(0,leng):
        t = 0
        res.append([0] * k)
        for j in range(0,n):
            if valid_k[i][j] == 1:
                res[i][t]=std[j]
                t+=1
    print(res)
    return res


    print(std)
# def core(m,n,k,j,s):
#     count_k = 1
#     K = np.zeros((1,n))
#     J = generate_strings(n,j)
#     for t in range(0,len(J)-1):
#         for v in range (0,count_k-1):
#             A = K[v] and J[t]





# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # # print(generate_strings(19, 6))
    # a= np.zeros((2,5))
    # str1 = '10111'
    # list1=['10111','10001','00110']
    #
    # d = np.array(list(list1[1]))
    # c = list(str1)
    # a[0][1]=1
    # a[1]=np.array(list(str1))
    # K = [[0] * 5]
    # J = [[1] * 5]
    # At = [K[0][idx] and J[0][idx] for idx in range(0, 5)]
    # print(At)
    # #print(xor(list1[0][0] , list1[0][0]))
    show(13,6,get(45,13,6,5,5))



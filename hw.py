import copy

dir = "test_case.txt"

#--------------------------------------------
# preparation
#--------------------------------------------

def read(dir):
    # read data w.r.t. given dir
    # if number of don't cares is 0, ignore last line in the file
    with open(dir, 'r') as f:
        num_var = int(f.readline())
        num_miniterms = int(f.readline())
        miniterms = f.readline()
        miniterms = miniterms.strip(' ').split(' ')
        miniterms = [int(x) for x in miniterms]
        if len(miniterms) != num_miniterms:
            raise ValueError("number of minterms entered is %d, wereas predefined number is %d" %(len(miniterms), num_miniterms))
        num_dcs = int(f.readline())
        if num_dcs != 0:
            dcs = f.readline()
            dcs = dcs.strip().split(' ')
            dcs = [int(x) for x in dcs]
            if len(dcs) != num_dcs:
                raise ValueError("number of dont cares entered is %d, wereas predefined number is %d" %(len(dcs), num_dcs))
        else:
            dcs = []
    return (num_var, miniterms, dcs)

#-------------------------------------------
# data process
#-------------------------------------------

def dec2bin(v, n):
    # transfer decimal to binary base
    # add 0 to fill n digits
    temp =[]
    temp2 = []
    while(v > 1):
        temp.append(v % 2)
        v //= 2
    temp.append(v)
    for i in range(n - len(temp)):
        temp2.append(0)
    for i in range(len(temp), 0, -1):
        temp2.append(temp[i-1])
    temp3 = ''
    for i in temp2:
        temp3 += str(i)
    return temp3

def bin2dec(v):
    # transfer binary to decimal base
    sum = 0
    n = len(v)
    for i,d in enumerate(v):
        if d == '1':
            sum += 2 ** (n-i-1)
    return sum

def stripdash(v):
    # strip dashes in binary form and return list of all possible counterparts
    # E.g. v = '10-1', return ['1001', '1011']
    lst = [v]
    n = v.count('-')
    while(len(lst) < 2 ** n):
        num = len(lst)
        for i in range(num):
            idx = lst[i].find('-')
            if idx != -1:
                lst.extend([lst[i].replace('-', '1', 1), lst[i].replace('-', '0', 1)])
                lst.remove(lst[i])

    return lst

def check_bin_dec(b, d):
    # check whether a decimal number conforms to the binary string
    # E.g. check_bin_dec('010-', 5) = True
    if d in [bin2dec(i) for i in stripdash(b)]:
        return True
    else:
        return False

def isgray(a, b):
    # check if the given binary strings are only different in one digit (gray code)
    count = 0
    idx = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            count+=1
            idx = i
        if count > 1:
            return None
    else:
        return idx

def replace(a, idx):
    # replace the only different digit with '-' if isgray is True
    ans = copy.copy(a)
    ans = list(ans)
    ans[idx] = '-'
    return ''.join(ans)

#--------------------------------------------
# reduce miniterms
#--------------------------------------------

def reduce(miniterms):
    # given list of miniterms, reduce them into prime miniterms by checking isgray() and sythesize into simpler form
    new_miniterms = []
    checked = [0 for i in range(len(miniterms))]
    for i in range(len(miniterms)):
        for j in range(i+1, len(miniterms)):
            result = isgray(miniterms[i], miniterms[j])
            if result != None:
                new_miniterms.append(replace(miniterms[i], result))
                checked[i] = 1
                checked[j] = 1

    for i in range(len(miniterms)):
        if checked[i] != 1 and miniterms[i] not in new_miniterms:
            new_miniterms.append(miniterms[i])

    return list(set(new_miniterms))

def get_prime(miniterms):
    # by doing reduce() until finally get a stable form of prime miniterms
    miniterms = sorted(miniterms)
    new_miniterms = []
    while(True):
        new_miniterms = reduce(miniterms)
        if sorted(new_miniterms) == sorted(miniterms):
            break
        miniterms = new_miniterms

    return new_miniterms

#------------------------------------------
# coverage optimization
#------------------------------------------

def cover(matrix, idx):
    # check if given indices of the columns can cover the whole matrix
    # duplicated by max_comp
    for i in matrix:
        sum = 0
        for j in idx:
            sum += i[j]
        if sum == 0:
            return False
    else:
        return True

def max_comp(matrix, idx):
    # given the matrix and list of indices (empty possible)
    # compute the scores for each row in the matrix indicating the complement to the current coverage
    # return the row with the max complement (least overlap) with the current coverage
    # return -1 if the coverage is already completed
    comp = [0 for i in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for k in range(len(matrix[i])):
            if k not in idx:
                sum = 0
                for j in idx:
                    comp[j] = -1
                    sum += matrix[i][j]
                if sum == 0 and matrix[i][k] != 0:
                    comp[k] += 1
    #print(comp)
    for i in comp:
        if i > 0:
            MAX = max(comp)
            return comp.index(MAX)

    return -1


def get_matrix(miniterms, d):
    # get matrix with col: miniterms and row: numbers expressed in the miniterms
    # if essential prime miniterms exists, append them to ans. Else ans is empty
    # by calculating max_comp of the current coverage given the matrix to get the reduced SOP
    row = []
    col = miniterms
    for i in miniterms:
        temp_lst = stripdash(i)
        for j in temp_lst:
            row.append(bin2dec(j))
    row = list(set(row) - set(d))
    matrix = [[] for i in range(len(row))]
    for i,d in enumerate(row):
        for j,b in enumerate(col):
            if check_bin_dec(b, d):
                matrix[i].append(1)
            else:
                matrix[i].append(0)
    #print(row, col, matrix)
    ans = []
    for i in matrix:
        temp = 0
        for j in i:
            temp += j
        if temp == 1:
            ans.append(i.index(1))

    if len(ans)>0:
        if cover(matrix, ans):
            return get_formula(ans, col)
    i = 0
    while(True):
        i = max_comp(matrix, ans)
        if i != -1:
            ans.append(i)
        else:
            break
    #print(ans)
    return get_formula(ans, col)
    #return row, col, matrix

#------------------------------------------
# output form
#------------------------------------------


def get_formula(idx, col):
    # get output form
    lookup = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    idx = list(set(idx))
    result = []
    ans = [col[i] for i in idx]
    for i in ans:
        temp = ''
        for j in range(len(i)):
            if i[j] == '-':
                continue
            temp += lookup[j]
            if i[j] == '0':
                temp += "'"
        result.append(temp)
    return '+'.join(result)


n, m, d = read(dir)
lst = []
for i in (m+d):
    lst.append(dec2bin(i, n))
print('reducing minterms...')
lst = get_prime(lst)
print('optimizing coverage...')
ans = get_matrix(lst, d)
print("Answer: %s"%ans)

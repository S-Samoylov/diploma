import math
import time

def printInline(s):
    print(s, end = '')

# decimal to binary
def decToBin(dec, n):
    result = []

    while True:
        result += [dec % 2]
        dec //= 2

        if dec == 0:
            break

    if len(result) != n:
        for i in range(n - len(result)):
            result += [0]

    return result[::-1]

def printCon(con, baseIndex):
    if con == 0 or con == 1:
        printInline(con)
        return

    for i in range(len(con)):
        if con[i] == 1:
            printInline('x' + str(i + baseIndex))

        if con[i] == 2:
            printInline('~x' + str(i + baseIndex))

def printPol(pol, baseIndex):
    for i in range(len(pol)):
        printCon(pol[i], baseIndex)

        if i != len(pol) - 1:
            printInline(' + ')

def parseZhigalkin(zhigalkin):
    pol = []
    n = int(math.log2(len(zhigalkin)))

    for i in range(len(zhigalkin)):
        if zhigalkin[i] == 1:
            binary = decToBin(i, n)

            if sum(binary) == 0:
                pol += [1]
            else:
                pol += [binary]

    return pol

def prepareConValues(n):
    # value of elementary & at arg
    def v(con, arg):
        v = 1
        check = 0

        for i in range(len(con)):
            check += con[i]

            if con[i] == 0:
                continue

            if con[i] == 1:
                v *= arg[i]
                continue

            v *= (arg[i] + 1) % 2

        if check == 0:
            return 0

        return v

    # vector of values of elementary &
    def truthVector(con):
        n = len(con)
        vector = []

        for i in range(2 ** n):
            vector += [v(con, decToBin(i, n))]

        return vector

    # iterate over elementary &
    def inc(con):
        n = len(con)

        for i in range(n):
            if i == 0:
                con[i] += 1

            if con[i] > 2:
                con[i] = 0

                if i != n - 1:
                    con[i + 1] += 1
                else:
                    return False

        return con

    conValues = []

    zeroCon = []

    zeroVal = []
    oneVal = []

    if n == 1:
        l = 2
    else:
        l = 2 ** n

    for i in range(l):
        zeroVal += [0]
        oneVal += [1]

        if i < n:
            zeroCon += [0]

    zeroVal = tuple(zeroVal)
    oneVal = tuple(oneVal)

    con = inc(zeroCon)
    while True:
        conValues += [{'con' : con.copy(), 'value' : tuple(truthVector(con))}]

        con = inc(con)

        if con == False:
            break

    conValues = sorted(conValues, key = lambda con: con['con'].count(0), reverse=True)

    conValues = [{'con' : 1, 'value' : oneVal}] + conValues
    conValues = [{'con' : 0, 'value' : zeroVal}] + conValues

    return conValues

def findZhegalkin(inputVec):
    n = int(math.log2(len(inputVec)))
    zhigalkin = inputVec.copy()

    # calculate zhigalkin
    for i in range(n):
        gap = 2 ** i
        j = gap
        while j < len(zhigalkin):
            for l in range(gap):
                zhigalkin[j] = (zhigalkin[j] + zhigalkin[j - gap]) % 2
                j += 1

            j += gap

    return zhigalkin

def findPol(inputVec):
    zhigalkin = findZhegalkin(inputVec)
    inputVec = tuple(inputVec)

    n = int(math.log2(len(inputVec)))

    conValues = prepareConValues(n)

    threshold = sum(zhigalkin)

    def walkTree(currentConNumber, currentPolValue, depth):
        if currentPolValue == inputVec:
            return [conValues[currentConNumber]['con']]

        if depth == threshold - 1:
            return False

        minPol = False
        for conNumber, con in enumerate(conValues[currentConNumber + 1:]):
            vecSum = tuple(map(lambda a, b: (a + b) % 2, con['value'], currentPolValue))

            result = walkTree(conNumber + currentConNumber + 1, vecSum, depth + 1)

            if result != False and (minPol == False or len(result) + 1 < len(minPol)):
                minPol = result + [conValues[currentConNumber]['con']]

        return minPol

    result = walkTree(0, conValues[0]['value'], 0)

    if result != False:
        result = result[::-1][1:]
        return result

    return parseZhigalkin(zhigalkin)

def shenon(inputVec, firstLevel = False):
    l = len(inputVec)

    if l <= 8:
        return findPol(inputVec)

    pol1 = shenon(inputVec[l // 2:])
    pol2 = shenon(inputVec[:l // 2])

    for i in range(len(pol1)):
        if pol1[i] == 1:
            newOne = [1]

            for j in range(int(math.log2(l // 2)) - 1):
                newOne += [0]

            pol1[i] = newOne
        else:
            pol1[i] = [1] + pol1[i]

    for i in range(len(pol2)):
        if pol2[i] == 1:
            newOne = [2]

            for j in range(int(math.log2(l // 2)) - 1):
                newOne += [0]

            pol2[i] = newOne
        else:
            pol2[i] = [2] + pol2[i]

    return pol1 + pol2

    
if (__name__ == "__main__"):
    inputFunc = []
    inputFuncString = input()

    for c in inputFuncString:
        if c == '0':
            inputFunc += [0]

        if c == '1':
            inputFunc += [1]

    zhigalkin = findZhegalkin(inputFunc)

    start = time.time()
    print(inputFunc)
    pol = shenon(inputFunc, True)
    end = time.time()

    print(inputFuncString)
    printPol(pol, 1)
    print('')
    print('Result length: ' + str(len(pol)))
    print('Zhigalkin length: ' + str(sum(zhigalkin)))
    print('Result time: ' + str(end - start))
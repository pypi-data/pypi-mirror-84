__author__ = 'miha_focsa'

from math import sqrt

def spl(*root):
    foundSolution = False
    primes = []
    nums = []
    start, end = 0, 100000
    sep = root[0].split('!')
    if sep[0] == '':
        root = sep[1]
        multp = None
    else:
        root = sep[1]
        multp = sep[0]
    for i in range(start, end + 1):
        if (i**(.5) == int(i**(.5))):
            nums.append(i)
    else:
        for i in range(100000):
            primes.append(i)
        else:
            for num in nums:
                if root == num:
                    foundSolution = True
                    return str(int(sqrt(num)))
                else:
                    pass
            else:
                for prime in primes:
                    if prime != 0:
                        if int(root) % int(prime) == 0:
                            r = int(root) / prime
                            s = sqrt(r)
                            items = str(s).split(".")
                            if foundSolution == True:
                                pass
                            else:
                                if len(str(float(items[1]))) > 3:
                                    pass
                                else:
                                    if multp == None:
                                        if str(float(items[1])) == '0.0':
                                            foundSolution = True
                                            mod_s = int(s)
                                            if mod_s != 1:
                                                if prime != 1:
                                                    return str(f"{mod_s}√{prime}")
                                                else:
                                                    mod_s = int(s)
                                                    return str(f"{mod_s}")
                                            else:
                                                return str(f"√{prime}")
                                    else:
                                        if str(float(items[1])) == '0.0':
                                            foundSolution = True
                                            mod_s = int(s) * int(multp)
                                            if mod_s != 1:
                                                if prime != 1:
                                                    mod_s = int(s) * int(multp)
                                                    return str(f"{mod_s}√{prime}")
                                                else:
                                                    mod_s = int(s) * int(multp)
                                                    mods_s = mod_s * prime
                                                    return str(f"{mods_s}") 
                                            else:
                                                return str(f"√{prime}")
                    else:
                        foundSolution = False

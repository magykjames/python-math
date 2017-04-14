# import operator
# import functools


# This function gets all the factors of a number, if there are any.
def getfactors(num):
    return [x for x in xrange(1, num + 1) if num % x == 0]


# This function generates as many prime numbers as possible in a given number
# of seconds.
def genprimes(seconds):
    import time
    true = True
    i = 1
    output = []
    ts = time.time()
    while true:
        gf = len(getfactors(i))
        if gf > 0 and gf <= 2:
            output.append(i)
        i += 1
        if time.time() - ts >= seconds:
            true = False
    print ('generated {} prime numbers in {} seconds at a rate of {} primes '
           'per second'.format(len(output), seconds, (len(output) / seconds)))
    return output


# This function tell us if a given number is prime or not.
def isprime(num):
    if not isinstance(num, (int, long)):
        print 'whole numbers only'
        return False
    if not num > 0:
        print 'positive numbers only'
        return False
    if num <= 2:
        return True
    factors = getfactors(num)
    if len(factors) <= 2:
        return True
    return False


# This function tells us all the lowest prime numbers you have to multiply
# together to form a given number.
def primefactors(num):
    # Get all the factors of the input.
    factors = getfactors(num)
    # Reject if it's a prime number or has no factors.
    if len(factors) <= 2:
        return factors
    # Create empty list to hold data.
    output = []
    # Setup a "while" loop to crawl over factors until options are exhausted.
    i = True
    while i:
        # Check to see if we have factors and they're all prime.
        # Add to output and stop loop if this is the case.
        if len(factors) > 1 and all(isprime(x) for x in factors[1:]):
            output += (factors[1:-1])
            i = False
        # Check if there's only one item in factors, add to output and break
        # if so.
        elif len(factors) == 1:
            output.append(factors[0])
            i = False
            break
        # Maybe there are no remaining factors, in that case break loop.
        elif not factors:
            i = False
            break
        # The first item in getfactors() is 1, so we're just going to look
        # at the second item.
        # Check if the last digit is divisible by the second item.
        # If so, append to output and get the factors of the last digit
        # divided by the second digit.
        if factors[-1] % factors[1] == 0:
            output.append(factors[1])
            factors = getfactors(factors[-1] / factors[1])
        else:
            # The last digit wasn't divisible by the second,
            # so let's get its factors.
            nf = getfactors(factors[-1])
            if len(nf) <= 2:
                # The last digit was a prime number, add it to output and stop
                # loop.
                output.append(factors[-1])
                i = False
                break
            else:
                # It wasn't a prime number, we have more factors to unpack, so
                # keep going.
                factors = nf
    return output


# This function returns x multiples of a give number.
def fxmult(num, x):
    output = []
    for i in range(1, x+1):
        output.append(num * i)
    return output


# This function tells us if a given multiple is a multiple of a given number.
def ismult(num, mult):
    if mult in getfactors(num):
        return True
    return False


# This function computes the total product of a list of numbers.
def prodlist(lst):
    if not lst:
        return None
    if len(lst) == 1:
        return lst[0]
    result = lst[0]
    for x in lst[1:]:
        if x:
            result *= x
    return result


# This function finds the least common multiples by multiplying all the
# prime factors together.
def lcmult(lst):
    # Make sure list has at least two elements and they're numbers.
    if len(lst) < 2 or any(not isinstance(x, (int, long)) for x in lst):
        return None
    # Get the prime factors of all the items in the list.
    pf = [primefactors(x) for x in lst]
    output = []
    # Look for items that have repeating prime factors.
    for x in pf:
        for p in x:
            multi = [m for m in x if m == p]
            # This element has multiple prime factors. Check output to see
            # if it has more prime factors than any other element.
            if len(multi) > 1:
                if len([o for o in output if o == p]) <= len(multi):
                    # Another element had multiple prime factors, but this one
                    # has more. Remove the previous entry to override.
                    output = filter(lambda x: x != p, output)
                # Add the multiple prime factors to output.
                output += multi
    # Add any other prime factors that aren't already in output.
    for x in pf:
        for p in x:
            if p not in output:
                output.append(p)
    # Sort it for best practices.
    output.sort()
    print output
    # We could use reduce and mul to get our result...
    # result = functools.reduce(operator.mul, output, 1)
    # Let's just use pure Python instead. Multiply all the elements together.
    # result = output[0]
    # for x in output[1:]:
    #     if x:
    #         result *= x
    return prodlist(output)


# This function finds the lowest common factor in a given list of numbers,
# if any exist.
def lcfactor(lst):
    # Make sure we have a list.
    if not isinstance(lst, list):
        return None
    # Make sure list has at least 2 elements.
    if len(lst) < 2:
        return None
    # Get the factors from each item in the list.
    lfactors = [getfactors(x) for x in lst]
    # Make sure all the factors returned valid results.
    if any(len(x) == 0 for x in lfactors):
        return None
    # Strip out the 1's and start with second element in each sublist.
    lfactors = [x[1:] for x in lfactors]
    for x in lfactors:
        for y in x:
            # If y is in all the factors, that's our least common factor.
            if len(lfactors) == len([i for i in lfactors if y in i]):
                return y
    return None


def isdiv(num, div):
    return True if num % div == 0 else False


def exnot(num):
    snum = list(str(num))
    snum.reverse()
    result = []
    for i in range(len(snum)):
        result.append('{}(1{})'.format(snum[i], '0' * i))
    result.reverse()
    result = ' + '.join(result)
    return result


# Round float to the nearest x places and return the result.
# This function includes all the different rounding options, but after
# testing, I found ROUND_HALF_UP results in the most common format.
def dec(num, places=2):
    from decimal import Decimal, getcontext
    # Convert the number of places to the Decimal equivalent...
    # ('.01') for 2 places, ('.1') for 1 place, etc.
    places = Decimal(10) ** -places
    # List of rounding options.
    rlist = [
        'ROUND_CEILING',
        'ROUND_DOWN',
        'ROUND_FLOOR',
        'ROUND_HALF_DOWN',
        'ROUND_HALF_EVEN',
        'ROUND_HALF_UP',
        'ROUND_UP',
        'ROUND_05UP'
        ]
    # Old print statement, removed for cleaner output.
    # print 'input: {}'.format(num)
    # We're going to populate the output with all possible rounding options.
    # Skip this for speed if necessary.
    output = {}
    # Loop over the list of rounding options and add each value to output.
    for x in rlist:
        getcontext().rounding = x
        dnum = float(Decimal(str(num)).quantize(places))
        # Old print statement for troubleshooting, this shows the behavior
        # of each rounding option.
        # print '{}: {}'.format(dnum, x)
        output[x] = dnum
    # Return the result with the chosen rounding option.
    return output['ROUND_HALF_UP']


# Find the lowest term in a given fraction; n over d.
def fraclt(n, d):
    # Get the prime factors of both the numerator and denominator.
    npf = primefactors(n)
    dpf = primefactors(d)
    # Loop over prime factors in numerator and remove matching
    # elements from denominator.
    for x in npf:
        if x in dpf:
            dpf.remove(x)
            npf.remove(x)
    # Loop over prime factors in denominator and remove matching
    # elements from numerator.
    for x in dpf:
        if x in npf:
            dpf.remove(x)
            npf.remove(x)
    # Return the products of remaining prime factors for numerator
    # and denominator. This is the lowest term.
    return (prodlist(npf), prodlist(dpf))


# Find the decimal place based on how many digits are past the decimal point.
# Return 0 if it's a whole number.
def decplace(num):
    # Convert the input to a string and split on the decimal.
    ns = str(num).split('.')
    # If there's only one element, we know there was nothing after the
    # decimal (or there was no decimal).
    if len(ns) == 1:
        return 0
    # Get the number of digits after the decimal.
    nsl = len(ns[1])
    # Place a 1 and add the number of zeroes equivalent to the number of
    # digits, so 1 digit gets 10, 2 digits gets 100, 3 digits gets 1000, etc.
    nsi = '1{}'.format('0' * nsl)
    # Convert back to int and return the result.
    return int(nsi)


# Find equivalent fractions. This is the reverse of the fraclt function.
# If operation results in a decimal for either numerator or denominator,
# convert the decimal to a fraction and include as an extra tuple.
def eqfrac(n, d, p):
    # To derive the equivalent, divide the desired place by the base
    # decimal, that becomes the multiplier.
    m = dec(p) / dec(d)
    # Multiply the numerator and denominator by the multiplier.
    nm = dec(n * m)
    dm = dec(d * m)
    # Create enoty output to populate results.
    output = []
    # Add the numerator if it's an integer.
    if nm.is_integer():
        output.append(int(nm))
    # If not, convert the decimal to a fraction (tuple) and add to output.
    else:
        nmt = (fraclt(int(nm % 1 * decplace(nm)), decplace(nm)))
        output += [int(nm), nmt]
    # Same thing for denominator...
    if dm.is_integer():
        output.append(int(dm))
    else:
        dmt = (fraclt(int(dm % 1 * decplace(dm)), decplace(dm)))
        output += [int(dm), dmt]
    # Return the result.
    return tuple(output)

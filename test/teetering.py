def balanceable(numbers):
    import itertools
    for permutation in itertools.permutations(numbers):
        for i in range(len(permutation)):
            if sum(permutation[0:i]) == sum(permutation[i:len(permutation)]):
                return True
    return False

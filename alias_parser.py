def get_modules(modulesPath):
    lines = open(modulesPath).readlines()
    pairs = [ln.strip().split(',') for ln in lines]
    return pairs

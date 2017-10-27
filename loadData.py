from router import Point


def load_interfere_ranges(file_path):
    results = []
    with open(file_path) as f:
        for line in f:
            if not line.split():
                continue
            line = line.strip()
            results.append(float(line))
    return results


def load_locations(file_path):
    results = []
    with open(file_path) as f:
        for line in f:
            if not line.split():
                continue
            line = line.strip()
            (x, y) = line.split(',')
            results.append(Point(float(x.strip()), float(y.strip())))
    return results


def load_parameters(file_path):
    a = 0
    b = 0
    with open(file_path) as f:
        for line in f:
            if not line.split():
                continue
            line = line.strip()
            if 'a' in line:
                (_, a_str) = line.split('=')
                a_str = a_str.strip()
                a = float(a_str)
            elif 'b' in line:
                (_, b_str) = line.split('=')
                b_str = b_str.strip()
                b = float(b_str)
    return a, b

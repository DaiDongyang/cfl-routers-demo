import loadData
import router
import sys
import random


variables = []
# locations = []
interfere_ranges = []
interfere_ranges_sq = []
a = 0.1
b = 0.1
loop_ceiling = 20000
# l_count = 0
interfere_ranges_path = "data/interfere_ranges.txt"
locations_path = "data/locations.txt"
parameters_path = "data/parameters.txt"


def load():
    global a, b, variables, interfere_ranges_sq, interfere_ranges
    locations = loadData.load_locations(locations_path)
    interfere_ranges = loadData.load_interfere_ranges(interfere_ranges_path)
    (a, b) = loadData.load_parameters(parameters_path)
    domain_len = len(interfere_ranges)
    variables = [router.Router(domain_len, p) for p in locations]
    interfere_ranges_sq = [x * x for x in interfere_ranges]


def append_variables(pos):
    global variables
    r = router.Router(len(interfere_ranges), router.Point(pos[0], pos[1]))
    variables.append(r)


def display_routers(vs, f=sys.stdout):
    for v in vs:
        print(v, file=f)


def check_pair_sq(r1, r2):
    """return true means satisfied constraint"""
    if r1.curr == r2.curr and r1.location.dist(r2.location) < interfere_ranges[r1.curr] + interfere_ranges[r1.curr]:
        return False
    return True


def check_routers(rs):
    for i in range(len(rs)-1):
        for j in range(i + 1, len(rs)):
            if not check_pair_sq(rs[i], rs[j]):
                return False
    result = True
    for r in rs:
        result = result and r.is_satisfied
    return result


def solve1(loop_limit):
    global variables
    loop_count = 0
    while not check_routers(variables) and loop_count < loop_limit:

        for r in variables:
            r.select = r.get_next_val()
            is_satisfied = True
            for r2 in variables:
                if r != r2 and not r.square_check(r2, interfere_ranges_sq[r.select]):
                    is_satisfied = False
                    break
            r.update_probs(a, b, is_satisfied)
            r.is_satisfied = is_satisfied
        for r in variables:
            r.curr = r.select
        loop_count = loop_count + 1
    return loop_count


def solve2(loop_limit):
    global variables
    loop_count = 0
    while not check_routers(variables) and loop_count < loop_limit:
        if loop_count % 100 == 0:
            print("solving", loop_count, "a", a, "b", b)
        for r in variables:
            r.select = r.get_next_val()
            r.curr = r.select
        is_satisfied = True
        for r in variables:
            for r2 in variables:
                if r != r2 and not r.check(r2, interfere_ranges[r.select] + interfere_ranges[r2.select]):
                    is_satisfied = False
                    break
            r.update_probs(a, b, is_satisfied)
            r.is_satisfied = is_satisfied
        loop_count = loop_count + 1
    return loop_count


def create_data(width, height, num, spec):
    file_prefix = "data/locations_created_"
    filename = file_prefix + str(num) + str(spec) + ".txt"
    with open(filename, "w") as outf:
        for _ in range(num):
            x = random.randint(0, width)
            y = random.randint(0, height)
            print(str(x) + ", " + str(y), file=outf)
    return filename


# test the variable number from lo to hi
def test_vLen(lo, hi):
    test_vlen_out = "output/test_vlen_out1.txt"
    wid = 800
    hei = 600
    global locations_path
    with open(test_vlen_out, "w") as outf:
        for i in range(lo, hi):
            locations_path = create_data(wid, hei, i, "1")
            load()
            l_count = solve2(loop_ceiling)
            print(l_count, file=outf)


# test the parameters
def test_parameters(ab_list_len):
    global a, b
    a_list = [x / ab_list_len for x in range(1, ab_list_len + 1)]
    b_list = [x / ab_list_len for x in range(1, ab_list_len + 1)]
    outfilename = "output/parameter_test.log"
    outfilename2 = "output/router_parameter_csv.csv"
    with open(outfilename, "w") as outf:
        with open(outfilename2, "w") as csvoutf:
            for a1 in a_list:
                for b1 in b_list:
                    load()
                    a = a1
                    b = b1
                    l_count = solve2(loop_ceiling)
                    print(l_count, end=",", file=csvoutf)
                    print(a, b, l_count, file=outf)
                print("\n", file=csvoutf)


# test the parameters, 为了避免偶然误差，生产filenum个实例，每个实例跑renum次
def test_parameters2(ab_list_len, filenum, renum):
    global a, b, locations_path
    a_list = [x / ab_list_len for x in range(1, ab_list_len + 1)]
    b_list = [x / ab_list_len for x in range(1, ab_list_len + 1)]
    outfilename = "output/parameter_test.log"
    outfilename2 = "output/router_parameter_csv.csv"
    tmpdatanames = []
    for k1 in range(filenum):
        tmpdataname = create_data(800, 600, 20, k1)
        tmpdatanames.append(tmpdataname)
    min_a = 0
    min_b = 0
    min_avg = loop_ceiling
    with open(outfilename, "w") as outf:
        with open(outfilename2, "w") as csvoutf:
            for a1 in a_list:
                for b1 in b_list:
                    avg_l = 0
                    for tdataname in tmpdatanames:
                        for _ in range(renum):
                            locations_path = tdataname
                            load()
                            a = a1
                            b = b1
                            l_count = solve2(loop_ceiling)
                            avg_l += l_count
                    avg_l = avg_l / (filenum * renum)
                    if avg_l < min_avg:
                        min_avg = avg_l
                        min_a = a
                        min_b = b

                    print(avg_l, end=",", file=csvoutf)
                    print(a, b, avg_l, file=outf)
                print(file=csvoutf)
    print("min_a,", min_a, "min_b", min_b, "min_avg", min_avg)


def get_location_created_filename(num, i):
    prefix = "data/locations_created_" + str(num)
    return prefix + str(i) + ".txt"


def test_channels(lo, hi):
    global locations_path, interfere_ranges, interfere_ranges_sq
    r = 90
    outfilename = "output/channel.txt"
    cs = []
    avgs = []
    for c in range(lo, hi):
        avg = 0
        with open("interfere_ranges.txt", "w") as interf:
            for _ in range(c):
                print(90, file=interf)
        for i in range(5):
            for _ in range(5):
                locations_path = get_location_created_filename(25, i)
                load()
            # interfere_ranges = [r for _ in range(c)]
            # interfere_ranges_sq = [x * x for x in interfere_ranges]
                l_count = solve2(loop_ceiling)
                # if l_count >= loop_ceiling:
                #     l_count = 0
                avg += l_count
        avg /= 25
        if avg == 0:
            avg = loop_ceiling
        cs.append(c)
        avgs.append(avg)
    with open(outfilename, "w") as outf:
        print(cs, file=outf)
        print(avgs, file=outf)





# if __name__ == "__main__":
#     test_channels(3, 20)
    # test_vLen(10, 30)
    # test_parameters2(10, 5, 5)



# load()
# l_count = solve2(loop_ceiling)
# print(l_count)
# for v in variables:
#     print(v)

# load()
# display_routers(variables[0])
# display_routers(variables[1])
# print(a, b)
# print(interfere_ranges_sq)

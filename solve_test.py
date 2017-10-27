import solve


def check_routers_test(rs):
    for i in range(len(rs)-1):
        for j in range(i + 1, len(rs)):
            result = solve.check_pair_sq(rs[i], rs[j])
            print(i, j, result)

solve.load()
solve.display_routers(solve.variables[0])
check_routers_test(solve.variables[0])

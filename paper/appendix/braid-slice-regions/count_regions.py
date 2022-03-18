import numpy as np
from math import factorial


np.set_printoptions(linewidth=400)
dtype = object


SS = None
TT = None


# Months after computing these numbers using the paper from Good and Tideman
# I came across this comprehensive write up on the subject of counting these regions
# by Warren D. Smith https://rangevoting.org/WilsonOrder.html
# The subject has a long history of independent (re)-discovery.
# Thanks to Shay Cohen for proposing I look up the numbers in oeis


def T(m, n):
    # Equation (6) from I.J.Good and T.N. Tideman
    # Look up precomputed Stirling numbers of the second kind
    # m objects
    # m - n indistinguishable parcels
    return TT[m, m-n]


def S(m, n):
    # Equation (5) from I.J.Good and T.N. Tideman
    # Look up precomputed Stirling numbers of the first kind
    assert n <= m
    # The formulation of S_m^n in Good and Tideman is different
    # compared to the formulation on wikipedia.
    # Since we filled the SS table using wikipedia recurrence
    # we need to adapt for use with Equation(5).
    #
    # https://en.wikipedia.org/wiki/Stirling_numbers_of_the_first_kind
    # Wikipedia coefficients of x^n: x(x-1)(x-2)...(x-m+1)
    # e.g. for m = 3 -> x(x-1)(x-2) = 2x + 3x^2 + 1x^3  (ignoring signs)
    # ┌─────┬───┬───┬────┬───┬───┐
    # │ n=  │ 0 │ 1 │ 2  │ 3 │ 4 │
    # ├─────┼───┼───┼────┼───┼───┤
    # │ m=0 │ 1 │ 0 │  0 │ 0 │ 0 │
    # │ m=1 │ 0 │ 1 │  0 │ 0 │ 0 │
    # │ m=2 │ 0 │ 1 │  1 │ 0 │ 0 │
    # │ m=3 │ 0 │ 2 │  3 │ 1 │ 0 │
    # │ m=4 │ 0 │ 6 │ 11 │ 6 │ 1 │
    # └─────┴───┴───┴────┴───┴───┘
    #
    # Good & Tideman (lets call variables n' and m'):
    # Coefficients of x^n': (1+x)(1+2x)..(1+(m'-1)x)
    # e.g. for m' = 3 -> (1+x)(1+2x) = 1 + 3x + 2x^2 
    # !! note flipped order of coefficients above !!
    # ┌─────┬───┬───┬────┬───┬───┐
    # │ n=  │ 0 │ 1 │ 2  │ 3 │ 4 │
    # ├─────┼───┼───┼────┼───┼───┤
    # │ m=0 │ 1 │ 0 │  0 │ 0 │ 0 │
    # │ m=1 │ 1 │ 0 │  0 │ 0 │ 0 │
    # │ m=2 │ 1 │ 1 │  0 │ 0 │ 0 │
    # │ m=3 │ 1 │ 3 │  2 │ 0 │ 0 │
    # │ m=4 │ 1 │ 6 │ 11 │ 6 │ 0 │
    # └─────┴───┴───┴────┴───┴───┘
    # Therefore: m'=m, n' = m-n
    return SS[m, m-n]


def N(R, P, M):
    # Equation (1) from I.J.Good and T.N. Tideman
    # Total number of regions
    if 0 <= R <= P <= M - 1:
        return T(M, P - R) * sum(S(M-P+R, nu) for nu in range(R+1))
    else:
        return factorial(M)


def B(R, P, M):
    # Equation (2) from I.J.Good and T.N. Tideman
    # Number of bounded regions
    if 0 <= R <= P <= M - 1:
        return T(M, P - R) * sum( (-1) ** (P - nu) * S(M-P+R, nu) for nu in range(R+1))
    else:
        return 0


def stirling_first_kind(N, K, signed=True):
    # https://en.wikipedia.org/wiki/Stirling_numbers_of_the_first_kind
    mem = np.zeros((N, K), dtype=dtype)
    mem[0, 0] = 1
    for n in range(N - 1):
        for k in range(1, K):
            if signed:
                mem[n+1, k] = - n * mem[n, k] + mem[n, k - 1]
            else:
                mem[n+1, k] = n * mem[n, k] + mem[n, k - 1]
    return mem


def stirling_second_kind(N, K):
    # https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind
    mem = np.zeros((N, K), dtype=dtype)
    mem[0, 0] = 1
    for n in range(N - 1):
        for k in range(1, K):
            mem[n+1, k] = k * mem[n, k] + mem[n, k - 1]
    return mem


if __name__ == "__main__":

    NUM_CLASSES = 10
    DIM = 10

    SS = stirling_first_kind(DIM+1, DIM+1, signed=False)
    TT = stirling_second_kind(DIM+1, DIM+1)

    # R = 1
    # d = 1
    # C = 2
    # total = N(R, d, C)
    # bounded = B(R, d, C)
    # print(total, bounded)


    counts = np.zeros((NUM_CLASSES, DIM), dtype=dtype)


    for num_classes in range(1, NUM_CLASSES+1):
        for dim in range(1, DIM+1):
            total = N(dim, dim, num_classes)
            bounded = B(dim, dim, num_classes)
            # Number of unbounded regions: https://oeis.org/A071223
            counts[num_classes-1, dim-1] = total - bounded

    cols = '& ' + ' & '.join(map(str, range(1, DIM+1)))
    header = """
        \\begin{table}[h!]
        \\scalebox{0.66}{
        \\begin{tabular}{cl| %s }
        \\toprule
        \\multicolumn{2}{c}{} %% remove vertical lines in this cell
                & \\multicolumn{ %d }{c}{\\textsc{Bottleneck dimensionality $d$}}  \\\\
        \\multicolumn{2}{c}{} %% remove vertical lines in this cell
         %s \\\\
        \\midrule
        \\multirow{ %d }{*}{\\rotatebox[origin=c]{90}{\\textsc{Number classes $|C|$}}}
    """ % (('l'*DIM), DIM, cols, DIM+1)
    print(header)

    for i, row in enumerate(counts):
        r = ' & '.join(map(str, row))
        print('\t\t& %d & %s\\\\' % (i+1, r))

    footer = """
        \\bottomrule
        \\end{tabular}
        }
        \\caption{Number of permutation regions defined by a bottlenecked softmax layer with no bias term. When $d \\geq |C| - 1$ all permutations corresponding to ways of ranking $|C|$ classes are feasible.}
        \\label{tab:numregions-nobias}
        \\end{table}
    """
    print(footer)


    for num_classes in range(1, NUM_CLASSES+1):
        for dim in range(1, DIM+1):
            total = N(dim, dim, num_classes)
            counts[num_classes-1, dim-1] = total

    print(header)
    for i, row in enumerate(counts):
        r = ' & '.join(map(str, row))
        print('\t\t& %d & %s\\\\' % (i+1, r))

    footer = """
        \\bottomrule
        \\end{tabular}
        }
        \\caption{Number of permutation regions defined by a bottlenecked softmax layer including a bias term. When $d \\geq |C| - 1$ all permutations corresponding to ways of ranking $|C|$ classes are feasible.}
        \\label{tab:numregions-bias}
        \\end{table}
    """
    print(footer)

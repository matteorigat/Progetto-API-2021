#!/usr/bin/env python3

import sys
import os
import random
import inputgen as ig

k_small = 10
k_big   = 1000

d_small = 4
d_big   = 400

def calc_nums(start, step):
    return [2**n for n in range(start, start + step*5, step)]

edge_p = 0.6

w_min = 0
w_max = 2**16 - 1

if __name__ == '__main__':
    root = os.path.join(sys.argv[1], 'input')

    os.makedirs(os.path.join(root, 'open'), exist_ok=True)
    os.makedirs(os.path.join(root, 'private'), exist_ok=True)

    random.seed(42)

    topk_multi = lambda n, topk_prob: ig.topk_any([ig.topk_endonly(n), ig.topk_prob(topk_prob)])

    ### Public Tests ###
    topk_p = 0.1
    # Test 1 (Normal)
    print('Generating test 1...', end='', flush=True)
    n = 2**5
    ig.gen_input_file(os.path.join(root, 'open', 'input.1'),
                      d_small, k_small, n, edge_p, w_min, w_max,
                      add_topk=ig.topk_endonly(n))

    # Test 2 (Normal Big)
    print(' done.\nGenerating test 2...', end='', flush=True)
    n = 2**5
    ig.gen_input_file(os.path.join(root, 'open', 'input.2'),
                      d_big, k_big, n, edge_p, w_min, w_max,
                      add_topk=ig.topk_endonly(n), decreasing=True)

    # Test 3 (Normal Big + TopK)
    print(' done.\nGenerating test 3...', end='', flush=True)
    n = 2**5
    ig.gen_input_file(os.path.join(root, 'open', 'input.3'),
                      d_big, k_big, n, edge_p, w_min, w_max,
                      add_topk=topk_multi(n, topk_p), decreasing=True)

    # Test 4 (Dijkstra)
    print(' done.\nGenerating test 4...', end='', flush=True)
    n = 2**5
    ig.gen_input_file(os.path.join(root, 'open', 'input.4'),
                      d_big, k_small, n, edge_p, w_min, w_max,
                      add_topk=ig.topk_endonly(n))

    # Test 5 (Insert)
    print(' done.\nGenerating test 5...', end='', flush=True)
    n = 2**10
    ig.gen_input_file(os.path.join(root, 'open', 'input.5'),
                      d_small, k_big, n, edge_p, w_min, w_max,
                      add_topk=ig.topk_endonly(n), decreasing=True)

    # Test 6 (Insert + TopK)
    print(' done.\nGenerating test 6...', end='', flush=True)
    n = 10
    ig.gen_input_file(os.path.join(root, 'open', 'input.6'),
                      d_small, k_big, n, edge_p, w_min, w_max,
                      add_topk=topk_multi(n, topk_p), decreasing=True)

    print(' done.')

    ### Private Tests ###
    topk_p = 0.003
    # Test 1 (Normal)
    print('Generating test 1...', end='', flush=True)
    n = 2**20 + 2**18 + 2**17
    ig.gen_input_file(os.path.join(root, 'private', 'input.1'),
                      d_small, k_small, n, edge_p, w_min, w_max,
                      add_topk=ig.topk_endonly(n))

    # Test 2 (Normal Big)
    print(' done.\nGenerating test 2...', end='', flush=True)
    n = 2**8
    ig.gen_input_file(os.path.join(root, 'private', 'input.2'),
                      d_big, k_big * 16, n, edge_p, w_min, w_max,
                      add_topk=ig.topk_endonly(n), decreasing=True)

    # Test 3 (Normal Big + TopK)
    print(' done.\nGenerating test 3...', end='', flush=True)
    n = 2**8
    ig.gen_input_file(os.path.join(root, 'private', 'input.3'),
                      d_big, k_big * 16, n, edge_p, w_min, w_max,
                      add_topk=topk_multi(n, topk_p), decreasing=True)

    # Test 4 (Dijkstra)
    print(' done.\nGenerating test 4...', end='', flush=True)
    n = 2**7 + 2**6 + 2**5
    ig.gen_input_file(os.path.join(root, 'private', 'input.4'),
                      d_big, k_small, n, edge_p, w_min, w_max,
                      add_topk=ig.topk_endonly(n))

    # Test 5 (Insert)
    print(' done.\nGenerating test 5...', end='', flush=True)
    n = 2**20 + 2**18
    ig.gen_input_file(os.path.join(root, 'private', 'input.5'),
                      d_small, k_big * 256, n, edge_p, w_min, w_max,
                      add_topk=ig.topk_endonly(n), decreasing=True)

    # Test 6 (Insert + TopK)
    print(' done.\nGenerating test 6...', end='', flush=True)
    n = 2**16 + 2**14 + 2**13
    ig.gen_input_file(os.path.join(root, 'private', 'input.6'),
                      d_small, k_big * 256, n, edge_p, w_min, w_max,
                      add_topk=topk_multi(n, topk_p), decreasing=True)

    print(' done.')

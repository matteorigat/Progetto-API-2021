#!/usr/bin/env python3

import random
import argparse

### Functions to decide when to output a TopK instruction

def topk_startonly():
    '''Add TopK only at the beginning.'''
    return lambda i: i == -1

def topk_endonly(mat_num):
    '''Add TopK at the end only.'''
    return lambda i: i == mat_num - 1

def topk_prob(p):
    '''Add TopK with a probability p.'''
    return lambda _: random.random() < p

def topk_every(every):
    '''Output TopK every `every' matrices.'''
    return lambda i: i >= 0 and i % every == every - 1

def topk_any(preds):
    '''Output TopK when any of the given predicates is True'''
    return lambda i: any(p(i) for p in preds)

### Output file generator

def gen_matrix(d, p, start, stop):
    return [[random.randrange(start, stop) if random.random() < p else 0 for _ in range(d)] for _ in range(d)]

def write_matrix(f, m):
    f.write('AggiungiGrafo\n')
    for row in m:
        f.write(','.join(map(str, row)) + '\n')

def gen_input_file(filename, d, k, mat_num, mat_p, mat_start, mat_stop,
                   add_topk=lambda _: False, decreasing=False, seed=None):
    write_topk = lambda f: f.write('TopK\n')

    if seed is not None:
        random.seed(seed)

    with open(filename, 'w') as f:
        f.write(f'{d} {k}\n')

        if add_topk(-1):
            write_topk(f)

        mat_step = max((mat_stop - mat_start) // mat_num, 1)
        real_start = mat_start
        real_stop = mat_stop
        p_step = mat_p / mat_num
        real_p = mat_p
        for i in range(mat_num):
            if decreasing:
                real_stop = mat_start + mat_step * max(mat_num - i, 1)
                real_start = max(mat_start, real_stop - mat_step)
                real_p = max(0.1, (mat_num - i) * mat_p)

            m = gen_matrix(d, real_p, real_start, real_stop)
            write_matrix(f, m)
            if add_topk(i):
                write_topk(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Nome del file da generare')
    parser.add_argument('d', type=int, help='Numero di nodi dei grafi da generare')
    parser.add_argument('k', type=int, help='Lunghezza della classifica')
    parser.add_argument('size', type=int, help='Numero di grafi da generare')

    parser.add_argument('--edge_prob', type=float, default=0.5,
                        help='Probabilità con cui inserire un arco nel grafo')
    parser.add_argument('--weight_min', type=int, default=0,
                        help='Valore minimo dei pesi dei grafi')
    parser.add_argument('--weight_max', type=int, default=2**32-1,
                        help='Valore massimo dei pesi dei grafi')
    parser.add_argument('--decreasing', action='store_true',
                        help='Rendi i pesi degli archi tendenzialmente decrescenti')

    parser.add_argument('--topk_start', action='store_true', help='Aggiungi comando TopK all\'inizio')
    parser.add_argument('--topk_end', action='store_true', help='Aggiungi TopK alla fine')
    parser.add_argument('--topk_every', type=int, help='Aggiungi TopK ogni TOPK_EVERY matrici')
    parser.add_argument('--topk_prob', type=float, help='Aggiungi TopK con una certa probabilità')
    args = parser.parse_args()

    if args.d < 1:
        print('Il valore del lato deve essere >= 1.')
        exit(1)
    if args.k < 1:
        print('La lunghezza della classifica deve essere >= 1.')
        exit(1)
    if args.size < 1:
        print('Il numero di matrici deve essere >= 1.')
        exit(1)
    if args.weight_min > args.weight_max:
        print('weight_min deve essere <= weight_max.')
        exit(1)
    if args.edge_prob < 0 or args.edge_prob > 1:
        print('edge_prob deve essere compreso tra 0 e 1.')
        exit(1)

    topk_preds = []
    if args.topk_start:
        topk_preds.append(topk_startonly())
    if args.topk_end:
        topk_preds.append(topk_endonly(args.size))
    if args.topk_every:
        if args.topk_every > 0:
            topk_preds.append(topk_every(args.topk_every))
        else:
            print('--topk_every richiede un argomento positivo.')
            exit(1)
    if args.topk_prob:
        if 0 <= args.topk_prob <= 1:
            topk_preds.append(topk_prob(args.topk_prob))
        else:
            print('--topk_prob richiede un argomento compreso tra 0 e 1.')
            exit(1)

    gen_input_file(args.filename, args.d, args.k, args.size, args.edge_prob,
                   args.weight_min, args.weight_max, topk_any(topk_preds), args.decreasing)

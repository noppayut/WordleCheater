from collections import Counter, defaultdict
from itertools import product
from typing import List


class Wordler:
    not_exist = 'NotExist'
    wrong_pos = 'WrongPos'
    correct = 'Correct'

    def __init__(self, word_path: str):
        with open(word_path, 'r') as f:
            self.words = f.read().upper().split('\n')

    def get_hint(self, word_states) -> List[str]:
        funcs = [filter_correct, filter_not_exist, filter_wrong_pos]
        alpha_pos_list = [word_states[state] for state in (self.correct, self.not_exist, self.wrong_pos)]
        cands = list(self.words)
        for f, alpha_pos in zip(funcs, alpha_pos_list):
            cands = f(cands, alpha_pos)

        return list(cands)


def filter_not_exist(candidates, alpha_pos):
    not_exist_alpha = set(alp for alp, _ in alpha_pos)
    return filter(lambda cand: len(set(cand).intersection(not_exist_alpha)) == 0, candidates)


def filter_correct(candidates, alpha_pos):
    return filter(lambda cand: all([cand[pos] == alpha for alpha, pos in alpha_pos]), candidates)


def filter_wrong_pos(candidates, alpha_pos):
    return filter(lambda cand: all([alpha in cand and cand[pos] != alpha for alpha, pos in alpha_pos]), candidates)


def find_best_guess(candidates):
    """
    Find most likely candidates
    :param candidates:
    :return:
    """
    if not candidates:
        return []
    most_probable_alps = get_most_probable_alps_at_each_pos(candidates)
    most_probable_seqs = list(product(*most_probable_alps))
    distances = calculate_distances(candidates, most_probable_seqs)
    min_dist = min(distances)
    best_guesses = [cand for cand, dist in zip(candidates, distances) if dist == min_dist]
    return best_guesses


def get_most_probable_alps_at_each_pos(candidates):
    def _get_most_probable_alps(alps_at_pos):
        mcs = Counter(alps_at_pos).most_common()
        max_occ = mcs[0][1]
        most_prob_alps_ = filter(lambda alp_occ: alp_occ[1] == max_occ, mcs)
        most_prob_alps = [alp for alp, occ in most_prob_alps_]
        return most_prob_alps

    alp_pos_dict = defaultdict(lambda: [])
    for cand in candidates:
        for i, c in enumerate(cand):
            alp_pos_dict[i].append(c)

    cand_len = len(candidates[0])
    most_probable_alps = [_get_most_probable_alps(alp_pos_dict[pos]) for pos in range(cand_len)]

    return most_probable_alps


def _calculate_distance(candidate, most_probable_seqs):
    def __calculate_distance_one(seq_1, seq_2):
        dist = sum([abs(ord(c_1) - ord(c_2)) for c_1, c_2 in zip(seq_1, seq_2)])
        return dist

    return min((__calculate_distance_one(candidate, mps) for mps in most_probable_seqs))


def calculate_distances(candidates, most_probable_seqs):
    return [_calculate_distance(candidate, most_probable_seqs) for candidate in candidates]

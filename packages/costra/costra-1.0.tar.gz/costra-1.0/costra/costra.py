"""Collection of various functions and function wrappers."""

import numpy as np
import os
import pkg_resources

from collections import defaultdict

DATA_FILE = pkg_resources.resource_filename("costra","data/data.tsv")


def get_sentences(data=DATA_FILE, tokenize=True):
    """Extract sentences from Costra 1.1. datafile to a list.
    Arguments:
        data: Path to Costra 1.1. datafile.
        tokenize: Tokenized/Untokenized sentences.
    """
    SENTENCES = []
    if not os.path.exists(data):
        raise ValueError("Missing sentence file '{}'".format(data))
    with open(data, "r") as sentence_file:
        for line in sentence_file:
            idx, number, transformation, sentence, tokenized_sentence, r1, r2, r3, r4 = line.strip('\n').split('\t')
            if tokenize:
                SENTENCES.append(tokenized_sentence)
            else:
                SENTENCES.append(sentence)
    return SENTENCES


def _get_comparisons_1(idx, a, b):
    """Collect comparisons of 1st type:
       If A < B and B < C, do their vector reflect this linearity, i.e do sim(A,B) > sim(A,C) and
       sim(B,C) > sim(A,C) hold?
    """
    if len(a) == 0:
        return []
    if len(b) == 0:
        return []
    out = []
    r1 = [int(x) for x in a.split(',')]
    r2 = [int(x) for x in b.split(',')]
    for i in r1:
        for j in r2:
            out.append([(idx, i), (i, j)])
            out.append([(idx, j), (i, j)])
    return out


def _get_comparisons_2(idx, a, b):
    """Collect comparisons of 2nd type:
       If A and B are too similar & B and C are too dissimilar, are vectors A and B closer to each
       other than vectors B and C?
    """
    if len(a) == 0:
        return []
    if len(b) == 0:
        return []
    out = []
    r1 = [int(x) for x in a.split(",")]
    r2 = [int(x) for x in b.split(",")]
    for i in r1:
        for j in r2:
            out.append([(idx, i), (idx, j)])
    return out


def _get_comparisons_3(idx, paraphrases, other):
    """Collect basic comparisons:
        Paraphrases should be closer to their seed than any transformation which significantly
        changes the meaning of the seed or modality of the seed.
    """
    out = []
    for p in paraphrases:
        for o in other:
            out.append([(idx, p), (idx, o)])
    return out


def _get_comparisons(data):
    """ Collect two types of comparisons from the Costra 1.1. dataset:
     - basic: paraphrase vs. significant change in meaning
     - advanced: comparisons based on the human judgement
    """

    basic = defaultdict(list)
    advanced = defaultdict(list)
    size = 0

    # first round - collecting indices and seeds
    with open(data, "r") as phil:
        current = 1
        roles = defaultdict(list)
        changes = {}
        for line in phil:
            size += 1
            idx, number, transformation, sentence, tokenized_sentence, r1, r2, r3, r4 = line.strip('\n').split('\t')
            idx, number = int(idx), int(number)
            changes[idx] = transformation
            if number != current:
                seed_idx = int(roles['seed'][0])
                paraphrases = [int(p_idx) for p_idx in roles['paraphrase']]
                for role in roles:
                    if role == 'seed' or role == 'paraphrase':
                        continue
                    basic[role].extend(_get_comparisons_3(seed_idx, paraphrases, roles[role]))
                roles = defaultdict(list)
                current = number

            roles[transformation].append(int(idx))
            comparisons_1 = _get_comparisons_1(idx, r1, r2)
            if transformation == 'seed':
                for c in comparisons_1:
                    advanced[changes[c[0][1]]].append(c)
            else:
                advanced[transformation].extend(comparisons_1)
            comparisons_2 = _get_comparisons_2(idx, r3, r4)
            advanced[transformation].extend(comparisons_2)

        # final
        seed_idx = int(roles['seed'][0])
        paraphrases = [int(p_idx) for p_idx in roles['paraphrase']]
        for role in roles:
            if role == 'seed' or role == 'paraphrase':
                continue
        basic[role].extend(_get_comparisons_3(seed_idx, paraphrases, roles[role]))

    return basic, advanced, size

def cosine_similarity(a, b):
    # Compute cosine similarity
    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    cos = dot / (norma * normb)
    return cos

def _get_unique_pairs(comparisons1,comparisons2):
    # Remove duplicate pairs
    unique_pairs = set()
    for pair in [x for y in comparisons1.values() for x in y]:
        unique_pairs.add(pair[0])
        unique_pairs.add(pair[1])
    for pair in [x for y in comparisons2.values() for x in y]:
        unique_pairs.add(pair[0])
        unique_pairs.add(pair[1])
    return unique_pairs


def _print_results(transformations, transformation_name, comparison_source, CACHE):
    # Compute accuracy and print result
    correct, total = 0, 0
    for transformation in transformations:
        for comparison in comparison_source[transformation]:
            total += 1
            if CACHE[comparison[0]] > CACHE[comparison[1]]:
                correct += 1
    print("%s %.3f" % (transformation_name.ljust(20), correct/ total))

def evaluate(embeddings, data=DATA_FILE):
    """Evaluate the embeddings.
    Arguments:
        embeddings: Numpy.ndarray with sentence embeddings.
        data: Path to Costra 1.1. datafile.
    """

    if not isinstance(embeddings,np.ndarray):
        raise ValueError("Embeddings are expected in numpy.ndarray format.")

    basic, advanced, size = _get_comparisons(data)

    if size != embeddings.shape[0]:
        raise ValueError("Size of embeddings doesn't match size of input data.")


    # There are repeated pairs of sentences in different comparisons, already counted distance is cached.
    unique_pairs = _get_unique_pairs(basic,advanced)
    CACHE = {x:cosine_similarity(embeddings[x[0]],embeddings[x[1]]) for x in unique_pairs}

    basic_changes = ["different meaning", "nonsense", "minimal change"]
    modality = ["ban","possibility"]
    time = ["past","future"]
    style = ["formal sentence","nonstandard sentence","simple sentence"]
    generalization = ["generalization"]
    opposite_meaning = ["opposite meaning"]

    print("transformation    accuracy")
    print("--------------------------")
    _print_results(basic_changes, "basic", basic, CACHE)
    _print_results(modality, "modality", basic, CACHE)
    _print_results(time, "time", advanced, CACHE)
    _print_results(style, "style", advanced, CACHE)
    _print_results(generalization, "generalization", advanced, CACHE)
    _print_results(opposite_meaning, "opposite meaning", advanced, CACHE)
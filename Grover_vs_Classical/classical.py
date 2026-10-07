import random

def black_box(candidate, winner):
    #The oracle: tells us whether candidate is the winning item.
    return candidate == winner

def linear_search(items, winner):
    #Scan in order, querying the black box, until the winner is found.
    #Returns the number of black-box queries used
    for i, item in enumerate(items):
        if black_box(item, winner):
            return i + 1
    raise ValueError("winner not present in items")


def benchmark_classical(n, trials=3000, seed=None):
    #Run trials: randomised linear searches over a list of size n and
    #return the empirical average query count, plus the worst case (n)
    rng = random.Random(seed)
    query_counts = []

    for _ in range(trials):
        items = list(range(n))
        rng.shuffle(items)
        winner = rng.choice(items)
        query_counts.append(linear_search(items, winner))

    avg_queries = sum(query_counts) / len(query_counts)
    return avg_queries, n  # (average, worst case)


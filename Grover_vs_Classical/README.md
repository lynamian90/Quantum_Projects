# Grover vs. Classical Search

A comparison of classical search against **Grover's
algorithm**, run and explained entirely in two Jupyter notebooks, open
either one on GitHub and you'll see the code, the circuit diagrams, and
the result plots.

## The idea

Say you have a list of N unsorted items and exactly one "winner." A
classical computer has no better strategy than checking items one at a
time - on average that takes **N/2** queries to a black-box oracle, and
N in the worst case.

Grover's algorithm solves the same problem on a quantum computer in
roughly **√N** oracle queries. This project
demonstrates that with actual simulated quantum circuits (via Qiskit),
not just the textbook formula.

## Notebooks

### [`Grover_Algorithm_Explained.ipynb`](notebooks/Grover_Algorithm_Explained.ipynb)
Builds the algorithm up piece by piece, with a plot or circuit diagrams:
1. The classical baseline (a linear search).
2. The quantum oracle - what it does and how to verify it with
   statevectors.
3. The diffuser ("inversion about the mean") and why it's needed.
4. A full worked 2-qubit example, with measurement result.
5. A generalized implementation that works for any number of qubits.
6. A demonstration of "overshooting" - why the number of iterations has
   to be chosen precisely, with a plot of success probability vs.
   iteration count.

### [`Scaling_Comparison.ipynb`](notebooks/Scaling_Comparison.ipynb)
Runs the classical search and the generalised Grover implementation
across N = 2 up to N = 256, and plots the O(N) vs O(√N) scaling gap on
both linear and log-log axes.
You can read `Grover_Algorithm_Explained` first for the conceptual walkthrough, or jump straight
to `Scaling_Comparison.ipynb` if you just want the results.



## Sample results

From `Scaling_Comparison.ipynb`, averaging the classical
search over 3000 randomized trials per N and running each Grover circuit
for 1024 shots:

| N   | Classical (avg) | Classical (worst case) | Grover (actual) | √N    |
|-----|------------------|--------------------------|-------------------|-------|
| 2   | ~1.5             | 2                        | 1                 | 1.41  |
| 4   | ~2.5             | 4                        | 1                 | 2.00  |
| 8   | ~4.6             | 8                        | 2                 | 2.83  |
| 16  | ~8.6             | 16                       | 3                 | 4.00  |
| 32  | ~16.7            | 32                       | 4                 | 5.66  |
| 64  | ~32.5            | 64                       | 6                 | 8.00  |
| 128 | ~64.8            | 128                      | 8                 | 11.31 |
| 256 | ~128.5           | 256                      | 12                | 16.00 |

Exact numbers vary slightly between runs since both the classical
benchmark and the quantum shots are randomized - re-running the notebook
will produce a similar but not identical table.

## Notes and caveats

- This runs on the Qiskit **Aer simulator**, not real quantum hardware -
  it demonstrates the algorithmic query complexity, not a physical
  runtime comparison. Real hardware today has noise, limited qubit
  counts, and connectivity constraints this doesn't model.
- The oracle here handles exactly one marked item. Grover's algorithm
  generalizes to multiple marked items (with a different iteration
  count), which is not covered here.



# Grover vs. Classical Search

A comparison of classical search against **Grover's algorithm**, built as a small Python package (`grover.py`, `classical.py`) and demonstrated in two
Jupyter notebooks.

## The idea

Say you have a list of N unsorted items and exactly one "winner." A classical
computer has no better strategy than checking items one at a time, on average
that takes **N/2** queries to a black-box/oracle (something that checks if you have the right item), and N in the worst case.

Grover's algorithm solves the same problem on a quantum computer in roughly
**√N** oracle queries. This project demonstrates that with actual simulated
quantum circuits (using Qiskit).

## Project structure

grover.py                          # Quantum code: oracle, diffuser, circuit builder, runner
classical.py                       # Classical linear search + benchmark
Grover_Algorithm_Explained.ipynb   # Conceptual walkthrough
Scaling_Comparison.ipynb           # O(N) vs O(√N) experiment and plots
README.md


### `grover.py`

| Function | What it does |
|----------|--------------|
| `build_oracle(n_qubits, winner)` | Phase oracle that flips the sign of the `\|winner>` state only |
| `build_diffuser(n_qubits)` | Reflection about the equal-superposition state (inversion about the mean) |
| `optimal_iterations(n_qubits)` | Optimal iteration count, r ≈ (π/4)·√N − 1/2 (minimum 1) |
| `build_grover_circuit(n_qubits, winner, iterations=None)` | Full circuit: Hadamards, oracle, diffuser, measurement |
| `run_grover(n_qubits, winner, iterations=None, shots=1024, seed=None)` | Runs the circuit on Aer; returns `(counts, iterations_used, success_probability)` |

### `classical.py`

| Function | What it does |
|----------|--------------|
| `linear_search(items, winner)` | Scans in order and returns the number of oracle queries used |
| `benchmark_classical(n, trials=3000, seed=None)` | Empirical average query count over random trials, returns `(average, worst_case)` |

## Notebooks

### [`Grover_Algorithm_Explained.ipynb`](Grover_Algorithm_Explained.ipynb)
Builds the algorithm up piece by piece, with plots and circuit diagrams:
1. The classical way (a linear search).
2. The quantum oracle - what it does and how to verify it with statevectors.
3. The diffuser ("inversion about the mean") and why it's needed.
4. A full worked 2-qubit example.
5. A generalized implementation (imported from `grover.py`) that works for any
   number of qubits.
6. A demonstration of "overshooting" - why the number of iterations has to be
   chosen precisely, with a plot of success probability vs. iteration count.

### [`Scaling_Comparison.ipynb`](Scaling_Comparison.ipynb)
Runs the classical search and the generalised Grover implementation across
N = 2 up to N = 256, and plots the O(N) vs O(√N) scaling on both linear and
log-log axes.

You can read `Grover_Algorithm_Explained` first for the explanation,
or go straight to `Scaling_Comparison` if you just want the results.

## Setup

Requires Python 3.10+ 

```bash
pip install qiskit qiskit-aer matplotlib numpy pandas
```

Run the notebooks from inside the `Grover_vs_Classical/` folder so that
`import grover` and `import classical` import correctly.

## Sample results

From `Scaling_Comparison.ipynb`, averaging the classical search over 3000
randomised trials per N and running each Grover circuit for 1024 shots:

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

Exact numbers vary slightly between runs since both the classical benchmark and
the quantum shots are randomized - re-running the notebook will produce a
similar but not identical table.

## Notes and caveats

- This runs on the Qiskit **Aer simulator**, not real quantum hardware - it
  demonstrates the query complexity, not the physical runtime
  comparison. Real hardware today has noise and limited qubit counts that this doesn't model.
- The oracle here handles exactly one marked item. Grover's algorithm
  generalizes to multiple marked items (with a different iteration count), which
  is not covered here.
- The "queries" counted for Grover are the number of oracle applications
  (iterations), compared against the number of black-box checks the classical
  search makes.
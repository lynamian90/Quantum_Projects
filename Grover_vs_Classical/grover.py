import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def build_oracle(n_qubits, winner):
    #Phase oracle: flips the sign of the |winner> basis state
    bits = format(winner, f"0{n_qubits}b")
    qc = QuantumCircuit(n_qubits, name="oracle")

    flip_qubits = [i for i, b in enumerate(reversed(bits)) if b == "0"]
    if flip_qubits:
        qc.x(flip_qubits)

    if n_qubits == 1:
        qc.z(0)
    else:
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)

    if flip_qubits:
        qc.x(flip_qubits)

    return qc.to_gate()


def build_diffuser(n_qubits):
    #Reflection about the superposition state |s>
    qc = QuantumCircuit(n_qubits, name="diffuser")
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))

    if n_qubits == 1:
        qc.z(0)
    else:
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits-1)
        qc.h(n_qubits-1)

    qc.x(range(n_qubits))
    qc.h(range(n_qubits))
    return qc.to_gate()


def optimal_iterations(n_qubits):
    #r ~= (pi/4)*sqrt(N) - 1/2, the grover iteration count
    n = 2 ** n_qubits
    return max(1, round((math.pi / 4) * math.sqrt(n) - 0.5))


def build_grover_circuit(n_qubits, winner, iterations=None):
    if iterations is None:
        iterations = optimal_iterations(n_qubits)

    oracle = build_oracle(n_qubits, winner)
    diffuser = build_diffuser(n_qubits)

    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))
    for _ in range(iterations):
        qc.append(oracle, range(n_qubits))
        qc.append(diffuser, range(n_qubits))
    qc.measure(range(n_qubits), range(n_qubits))
    return qc


def run_grover(n_qubits, winner, iterations=None, shots=1024, seed=None):
    if iterations is None:
        iterations = optimal_iterations(n_qubits)
    backend = AerSimulator(seed_simulator=seed)
    qc = build_grover_circuit(n_qubits, winner, iterations=iterations)
    transpiled = transpile(qc, backend)
    counts = backend.run(transpiled, shots=shots).result().get_counts()
    winner_bits = format(winner, f"0{n_qubits}b")
    success_probability = counts.get(winner_bits, 0) / shots
    return counts, iterations, success_probability
"""Functions for estimating path flows."""

from .matrix import Matrix, Vector

__all__ = ['estimate']

def estimate(paths, movements, movement_flows, niter=100):
    """Estimate path flows.

    Args:
        paths: a sequence of Path instances
        movements: a sequence of Movement instances
        movement_flows: a sequence of numbers, aligning with ``movements``
        niter: the number of iterations (optional)

    Returns
        path flows
    """

    incidence_matrix = Matrix([
        [
            movement.incidence_count(path)
            for path in paths
        ]
        for movement in movements
    ])
    return ipf(incidence_matrix, movement_flows, niter)


def ipf(A, b, niter=100):
    """An implementation of the iterative proportional fitting (IPF)
    algorithm.

    Args:
        A: the incidence matrix
        b: the target movement flows
        niter: the number of iterations (optional)

    Returns:
        path flows
    """
    A = Matrix(A)
    b = Vector(b)
    current_x = Vector.ones(A.shape[1])

    for _ in range(niter):
        for i in range(len(b)):
            current_b = A @ current_x
            ratio = b[i] / current_b[i]
            for j in range(len(current_x)):
                if A[i][j] != 0:
                    current_x[j] = current_x[j] * ratio

    return list(current_x)

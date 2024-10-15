"""Class and functions for specifying movements and getting incidence counts."""

from .incidence import incidence_count

__all__ = ["Movement"]

class Movement:
    """Specifies a path sub-sequence.

    A movement specifies a sub-path sequence on a network. Movements are
    specified using a list. Within the list an Ellipsis (``...``) will match
    zero or more nodes. Any other value must match a node in the path exactly.
    Each path on the network is incident on the movement zero or more times. For
    example if the movement is ``[..., 2, 3, ...]``, the paths ``[1, 2, 3]`` and
    ``[1, 2, 3, 4]`` are each incident once on the movement; the path ``[2, 3,
    2, 3]`` is incident twice; and the path ``[4, 5, 6]`` is incident zero
    times. These examples and others are listed in the table below.

    ===================== ================ ===============
    movement              path             incidence count
    ===================== ================ ===============
    ``[..., 2, 3, ...]``  ``[1, 2, 3]``     1
    ``[..., 2, 3, ...]``  ``[1, 2, 3, 4]``  1
    ``[..., 2, 3, ...]``  ``[2, 3, 2, 3]``  2
    ``[..., 2, 3, ...]``  ``[4, 5, 6]``     0
    ``[2, 3]``            ``[1, 2, 3]``     0
    ``[2, 3]``            ``[2, 3]``        1
    ``[2, 3]``            ``[2]``           0
    ``[..., 1]``          ``[1]``           1
    ``[..., 1]``          ``[2, 1]``        1
    ``[..., 1]``          ``[2, 1, 0]``     0
    ``[1, ..., 5]``       ``[1, 5]``        1
    ``[1, ..., 5]``       ``[1, 2, 5]``     1
    ``[1, ..., 5]``       ``[1, 2, 3, 5]``  1
    ``[1, ..., 5]``       ``[2, 1, 5]``     0
    ===================== ================ ===============

    A concrete example of movements are turns at a highway intersection. For
    example, the left turn from a particular leg of the intersection can be
    modeled as a sequence of three nodes which form a movement.

    Movements are used to represent the observable portion of paths. One cannot
    observe a vehicle traveling along the entire length if its path, but shorter
    movements are observable, so the flow on the movement can be measured. These
    movement flow measurements can then be used to estimate path flows.

    Typically users should intialize movements directly in order to model
    the movements that they have measured flows for.

    Movement instances are used in the :func:`felt.estimate.estimate` function
    to help construct a path-movement incidence matrix.

    Args:
        movement: the movement specification list. May include ellipsis.

    Examples:
        Initialize a Movement instance:

        >>> from felt import Movement
        >>> movement = Movement([..., 2, 3, ...])
    """
    def __init__(self, movement):
        self._movement = movement

    def incidence_count(self, path):
        """Get the incidence count for a path on the movement.

        The incidence count is the number of times that a path is incident on a
        movement. Normally the count is either zero or one, but it may be two or
        more in some cases.

        This method is used in the :func:`felt.estimate.estimate` function
        to compute values to fill the incidence matrix.

        Args:
            path: a list or Path instance

        Returns:
            int: the incidence count; always non-negative.

        Examples:
            Get an incidence count:

            >>> from felt import Movement
            >>> movement = Movement([..., 2, 3, ...])
            >>> movement.incidence_count([1, 2, 3])
            1

        """
        return incidence_count(self._movement, list(path.node_names))

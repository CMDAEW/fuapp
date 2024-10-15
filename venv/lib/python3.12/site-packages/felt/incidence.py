"""Functions for computing incidence count. Supports the
:meth:`felt.movement.Movement.incidence_count` method"""

__all__ = ['incidence_count']

class NoMovement(Exception):
    """Used in incidence counts functions to signal that the path
    is not incident on the movement.

    Users should not use this exception.
    """

def incidence_count(movement, path):
    """Given a movement and a path, calculate the number of times the path
    is incident on the matrix.

    Users should not call this function directly, but should use
    :meth:`felt.movement.Movement.incidence_count`.
    """
    movement = movement[:]
    path = path[:]

    if not movement:
        raise ValueError('movement cannot be empty')
    if not path:
        raise ValueError('path cannot be empty')

    count = 0
    while path:
        try:
            path = _match_movement(movement, path)
        except NoMovement:
            break
        else:
            count += 1
    return count

def _match_movement(movement, path):
    """Try to match the movement to the path once.

    Users should not call this function.
    """
    while movement:
        movement, path = _match_movement_elem(movement, path)
    if movement:
        raise NoMovement()
    return path

def _match_movement_elem(movement, path):
    """Try to match a single element from a movement to the path.

    Users should not call this function.
    """
    movement = movement[:]
    path = path[:]

    if movement[0] == Ellipsis:
        while movement and (movement[0] == Ellipsis):
            movement.pop(0)
        if not movement:
            return [], path
        x = movement.pop(0)
        try:
            i = path.index(x)
        except ValueError:
            raise NoMovement()
        else:
            return  movement, path[i+1:]
    else:
        if not path:
            raise NoMovement()
        x = movement.pop(0)
        if x == path[0]:
            return movement, path[1:]
        raise NoMovement()

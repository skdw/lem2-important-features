class DataRow:
    def __init__(self, c_attrs, d_attrs):
        """Data row

        Args:
            c_attrs (dict): conditions
            d_attrs (bool): decision
        """
        self.c_attrs = c_attrs
        self.d_attrs = d_attrs


class DecisionTable:
    def __init__(self, U: set(DataRow), C: set, D: set(bool)):
        """Decision table

        Args:
            U (set(DataRow)): objects
            C (set): condition attributes
            D (set(bool)): decision attributes
        """

        self.U = U
        self.C = C
        self.D = D


def lower_bound(T: set) -> set:
    """[summary]

    Args:
        T (set): [description]

    Returns:
        set: [description]
    """
    return T


def upper_bound(T: set) -> set:
    """[summary]

    Args:
        T (set): [description]

    Returns:
        set: [description]
    """
    return T


def lem2(X: DecisionTable, C: set) -> set:
    """LEM2 algorithm

    Args:
        X (DecisionTable): upper or lower decisive class approximation
        C (set): condition attributes

    Returns:
        set: single local X ...
    """
    G = X

    # T - set of conditions
    T = set()
    for q in C:
        vq = X.C[q]
        t = (q, vq) # elementary condition
        T.add(t)

    def abscl(t):
        # u: DataRow from X.U
        (q, vq) = t
        return set(u for u in X.U if u.c_attrs[q] == vq)

    # [t]
    t_absclass = map(abscl, T)

    

    return set()



C = set('headache', 'fever')
D = set('flu')

U1c = {'headache': True, 'fever': 'normal'}
U1d = False
U1 = DataRow(U1c, U1d)

U2c = {'headache': True, 'fever': 'high'}
U2d = True
U2 = DataRow(U1c, U1d)

U = set(U1, U2)

T = DecisionTable(U, C, D)

X = lower_bound(T)
res = lem2(X, C)

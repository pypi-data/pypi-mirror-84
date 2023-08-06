from dataclasses import fields


class OrderedValueRange:
    def __init__(self, upper_bound=None, lower_bound=None,
                 ub_include=False, lb_include=True, equality=lambda x, y: x == y):
        self._upper_bound = upper_bound
        self._ub_included = ub_include

        self._lower_bound = lower_bound
        self._lb_included = lb_include
        self._equality = equality

    def upto(self, upper_bound, ub_include=False):
        self._upper_bound = upper_bound
        self._ub_included = ub_include

    def at_least(self, lower_bound, lb_include=True):
        self._lower_bound = lower_bound
        self._lb_included = lb_include

    def between(self, lower_bound, upper_bound, ub_include=False, lb_include=True):
        self._lower_bound = lower_bound
        self._lb_included = lb_include

        self._upper_bound = upper_bound
        self._ub_included = ub_include

    def is_included(self, value):
        if self._upper_bound and value > self._upper_bound:
            return False

        if not self._ub_included and self._equality(value, self._upper_bound):
            return False

        if self._lower_bound and value < self._lower_bound:
            return False

        if not self._lb_included and self._equality(value, self._lower_bound):
            return False

        return True

    def __str__(self):
        ret = 'lambda x: '
        if self._lower_bound:
            ret = f'{self._lower_bound}'
            ret += ' <= ' if self._lb_included else ' < '
        ret += 'x'
        if self._upper_bound:
            ret += ' <= ' if self._ub_included else ' < '
            ret += f'{self._upper_bound}'

        return ret

    def __repr__(self):
        return self.__str__()


def chain_clz_setters(clz):
    fs = fields(clz)

    def make_chainable(fi):
        def set_value(obj, value):
            setattr(obj, fi, value)
            return obj

        return set_value

    for f in fs:
        setattr(clz, f.name + '_as', make_chainable(f.name))

    return clz


def chain_obj_setters(target_obj):
    field_names = tuple(vars(target_obj).keys())

    def make_chainable(fi):
        def set_value(value):
            setattr(target_obj, fi, value)
            return target_obj

        return set_value

    for f in field_names:
        setattr(target_obj, f + '_as', make_chainable(f))

    return target_obj

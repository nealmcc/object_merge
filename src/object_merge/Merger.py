class Merger(object):
    def __init__(self, a, b, resolver=None):
        self._a = a
        self._b = b
        self._resolver = resolver

    def merge_into(self, c):
        c['merged_from'] = (self._a['id'], self._b['id'])
        c = {**c, **self.only_a(), **self.only_b()}
        for key in self.common_keys():
            self.merge_field(c, key)
        return c

    def only_a(self):
        a_only_keys = set(self._a).difference(self._b)
        return {k: self._a[k] for k in a_only_keys}

    def only_b(self):
        b_only_keys = set(self._b).difference(self._a)
        return {k: self._b[k] for k in b_only_keys}

    def common_keys(self):
        for key in set(self._a).intersection(self._b):
            if key != 'id' and key != 'merged_from':
                yield key

    def merge_field(self, c, key):
        ''' merges a single field into c '''
        if (self._a[key] == self._b[key]):
            c[key] = self._a[key]
        else:
            try:
                a_list = [val for val in self._a[key]]
                b_list = [val for val in self._b[key]]
                c[key] = a_list + b_list
            except TypeError:
                # at least one of the values isn't enumerable.
                # time for manual resolution
                self.resolve_conflict(c, key)

    def resolve_conflict(self, c, key):
        if self._resolver:
            self._resolver(self._a, self._b, c, key)
        else:
            # without being given a resolution strategy, we just pick a:
            c[key] = self._a[key]

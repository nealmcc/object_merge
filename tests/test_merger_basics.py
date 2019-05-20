import random
from src.object_merge.Merger import Merger

a = {
    'id': 'a',
    'url': ['https://website.com/login'],
    'username': 'foo',
    'password': 'bar',
    'colour': 'orange',
    'fav_number': 42
}
b = {
    'id': 'b',
    'url': ['https://subdomain.website.com/login'],
    'username': 'foo',
    'password': 'bar',
    'fruit': 'orange',
    'fav_number': 32
}


def random_resolver(a, b, c, key):
    ''' simulates the user picking either a or b to resolve the merge '''
    source = random.choice([a, b])
    c[key] = source[key]


class TestMergerBasics(object):
    """ Starting scenarios for TDD """

    def test_merges_two_dictionaries(self):
        testme = Merger(a, b)
        c = testme.merge_into({'id': 'c'})
        assert c['id'] == 'c'
        assert c['merged_from'] == ('a', 'b')
        assert c['url'] == ['https://website.com/login',
                            'https://subdomain.website.com/login']
        assert c['fav_number'] == a['fav_number']

    def test_uses_a_delegate_for_conflict_resolution(self):
        testme = Merger(a, b, random_resolver)
        c = testme.merge_into({'id': 'c'})
        assert c['id'] == 'c'
        assert c['merged_from'] == ('a', 'b')
        assert c['url'] == ['https://website.com/login',
                            'https://subdomain.website.com/login']
        assert c['fav_number'] == 42 or c['fav_number'] == 32

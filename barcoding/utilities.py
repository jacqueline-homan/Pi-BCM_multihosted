import logging
import hashlib
import os


def isValid(nums):
    ''' Returns boolean indicating if check digit is correctly calculated using mod 10 algorithm.
    >>> isValid('012345678901')
    False
    >>> isValid('012345678905')
    True
    '''
    if not nums: return False
    cd1  = nums[-1]
    meat = nums[0:-1][::-1]#cut cd away, reverse string, since x3 always applays from right (BC)
    odds = sum(map(lambda i: int(i)*3,list(meat[0::2])))
    evns = sum(map(lambda i: int(i),list(meat[1::2])))
    cd2  = str(10 - ((odds + evns) % 10))[-1]# 0 if 10 or reminder
    return cd1 == cd2


def from_14d(bc, type):
    if len(bc) == 14:
        bc = bc[1:]
        if type == 'UPCA':
            bc = bc[1:]
    return bc

def to_14d(bc,type):
    if len(bc) < 14:
        bc = "0" + bc
        if type == "UPCA":
            bc = "0" + bc
    return bc

def prev_next(bc, prefix):
    bc = bc[:-1]
    serial = bc[len(prefix):]
    prev_bc = int(serial) - 1
    if prev_bc < 0:
        prev_bc = None
    else:
        f = '{0:0%d}' % len(serial)
        prev_bc = normalize('EAN13', prefix + f.format(prev_bc))
    next_bc = int(serial) + 1
    if len(str(next_bc)) > len(serial):
        next_bc = None
    else:
        f = '{0:0%d}' % len(serial)
        next_bc = normalize('EAN13', prefix + f.format(next_bc))
    return prev_bc, next_bc

def normalize(kind,value):
    ''' Normalizes EAN/UPC to required length
    >>> normalize('UPCA','123')
    '123000000006'
    >>> normalize('EAN13','123')
    '1230000000000'
    >>> normalize('ISBN13','123')
    '9781230000008'
    '''
    if kind == "UPCA":
        value1 = ''.join(list(filter(lambda x: x.isdigit(), value)))
        value2 = '{0:0<12}'.format(value1)[0:12]
        value3 = getValid(value2)
        return value3
    if kind == "EAN13":
        value1 = ''.join(list(filter(lambda x: x.isdigit(), value)))
        value2 = '{0:0<13}'.format(value1)[0:13]
        value3 = getValid(value2)
        return value3
    if kind == "ISBN13":
        value1 = ''.join(list(filter(lambda x: x.isdigit(), value)))
        if value1.find('978') == 0:
            value2 = value1
        else:
            value2 = "978%s" % value1
        value3 = '{0:0<13}'.format(value2)[0:13]
        value4 = getValid(value3)
        return value4
    if kind == "GTIN14":
        value1 = ''.join(list(filter(lambda x: x.isdigit(), value)))
        value2 = '{0:0<14}'.format(value1)[0:14]
        value3 = getValid(value2)
        return value3
    raise Exception("wrong kind!")

def getValid(nums):
    ''' Fixes incorrect number replacing the CD with the corrected one.
    >>> getValid('012345678901')
    '012345678905'
    '''
    if not nums: return None
    cd1  = nums[-1]
    meat = nums[0:-1][::-1]#cut cd away, reverse string, since x3 always applays from right (BC)
    odds = sum(map(lambda i: int(i)*3,list(meat[0::2])))
    evns = sum(map(lambda i: int(i),list(meat[1::2])))
    cd2  = str(10 - ((odds + evns) % 10))[-1]# 0 if 10 or reminder
    return nums[0:-1] + cd2

def make_omlet(b):
    """ Hashes up vital barcode params and presents the as a hash
    """
    s=''.join([str(i) for i in [b.gtin,b.kind,b.size,b.bwr,b.rqz,b.pmk,b.price,b.name,b.debug]])
    return hashlib.sha1(s).hexdigest()[0:5]

# def get_spam(l):
#     """
#     >>> get_spam({'a':1,'b':'foo'})
#     'acbd1'
#     """
#     s = ''
#     for item in l.values():
#         if type(item) in [str,float,list]:
#              s += str(item)
#     hash = md5.new()
#     hash.update(s)
#     value = hash.hexdigest()[0:5]
#     return value

def check_dir(s):
    media_root = '/tmp' # FIXME
    d = '%s/%s' % (media_root,s)
    logging.getLogger().debug("will check %s" % d)
    if not os.path.exists(d):
        logging.getLogger().debug("will generate %s" % d)
        os.makedirs(d)
    else:
        logging.getLogger().debug("directory %s exists -- do nothing" % d)
    return d

class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.

        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'
        >>> del o.z
        Traceback (most recent call last):
            ...
        AttributeError: 'z'

    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'

storage = Storage

def storify(mapping, *requireds, **defaults):
    """
    Creates a `storage` object from dictionary `mapping`, raising `KeyError` if
    d doesn't have all of the keys in `requireds` and using the default
    values for keys found in `defaults`.

    For example, `storify({'a':1, 'c':3}, b=2, c=0)` will return the equivalent of
    `storage({'a':1, 'b':2, 'c':3})`.

    If a `storify` value is a list (e.g. multiple values in a form submission),
    `storify` returns the last element of the list, unless the key appears in
    `defaults` as a list. Thus:

        >>> storify({'a':[1, 2]}).a
        2
        >>> storify({'a':[1, 2]}, a=[]).a
        [1, 2]
        >>> storify({'a':1}, a=[]).a
        [1]
        >>> storify({}, a=[]).a
        []

    Similarly, if the value has a `value` attribute, `storify will return _its_
    value, unless the key appears in `defaults` as a dictionary.

        >>> storify({'a':storage(value=1)}).a
        1
        >>> storify({'a':storage(value=1)}, a={}).a
        <Storage {'value': 1}>
        >>> storify({}, a={}).a
        {}

    """
    def getvalue(x):
        if hasattr(x, 'value'):
            return x.value
        else:
            return x

    stor = Storage()
    for key in requireds + tuple(mapping.keys()):
        value = mapping[key]
        if isinstance(value, list):
            if isinstance(defaults.get(key), list):
                value = [getvalue(x) for x in value]
            else:
                value = value[-1]
        if not isinstance(defaults.get(key), dict):
            value = getvalue(value)
        if isinstance(defaults.get(key), list) and not isinstance(value, list):
            value = [value]
        setattr(stor, key, value)

    for (key, value) in defaults.iteritems():
        result = value
        if hasattr(stor, key):
            result = stor[key]
        if value == () and not isinstance(result, tuple):
            result = (result,)  # pragma: no cover
        setattr(stor, key, result)

    return stor

# def _test():
#     import doctest
#     doctest.testmod()

# if __name__ == "__main__":
#     import sys
#     from django.core.management import setup_environ
#     sys.path.append("..")
#     import settings
#     setup_environ(settings)
#     _test()

'''

Argument Formatters

'''
from collections import namedtuple
from . import util


DEFAULT_CLI = 'fire'


NoArgVal = '((((SLURMJOBS: NO ARG VALUE))))'


class Arg(namedtuple('Arg', 'key value format')):
    def __new__(self, key, value=NoArgVal, format=True):
        return super().__new__(self, key, value, format)


class ArgGroup(namedtuple('Arg', 'args kwargs')):
    def __new__(self, *a, **kw):
        return super().__new__(self, a, kw)


def flat_join(xs):
    return ' '.join(str(x) for x in util.flatten(xs) if x)


class Argument(util.Factory):
    prefix = suffix = ''

    @classmethod
    def get(cls, key='fire'):
        # key=fire -> FireArgument, key=None -> Argument
        return cls.__children__(suffix='argument').get(key.lower()) if key else cls

    @classmethod
    def _format_args(cls, *args, **kw):
        args = [cls.format_arg_or_group(v) for v in args]
        kw = {k: cls.format_arg_or_group(k, v) for k, v in kw.items()}
        return args, kw

    @classmethod
    def build(cls, cmd, *a, **kw):
        a2, kw2 = cls._format_args(*a, **kw)
        values = {f'_{k}': v for k, v in dict(enumerate(a), **kw).items()}
        all_ = flat_join([cls.prefix] + a2 + list(kw2.values()) + [cls.suffix])
        return cmd.format(*a2, **kw2, __all__=all_, **values)

    @classmethod
    def build_args(cls, *a, **kw):
        return cls.build('{__all__}', *a, **kw)

    @classmethod
    def format_arg_or_group(cls, k, v=NoArgVal):
        value = k if v is NoArgVal else v
        if isinstance(value, ArgGroup):
            return cls.format_group(value)
        if isinstance(value, Arg):
            if not value.format:
                return value.key if value.value is NoArgVal else value.value
            k, v = value.key, value.value
        return cls.format_arg(k, v)

    @classmethod
    def format_group(cls, v):
        args, kw = cls._format_args(*v.args, **v.kwargs)
        return flat_join(args + list(kw.values()))

    @classmethod
    def format_arg(cls, k, v=NoArgVal):
        return cls.format_value(k) if v is NoArgVal else cls.format_value(v)

    @classmethod
    def format_value(cls, v):
        return util.shlex_repr(v)



class FireArgument(Argument):
    kw_fmt = '--{key}={value}'

    @classmethod
    def format_arg(cls, k, v=NoArgVal):
        if v is NoArgVal:
            return cls.format_value(k)
        return cls.kw_fmt.format(key=k, value=cls.format_value(v))



class ArgparseArgument(Argument):
    short_opt, long_opt = '-', '--'

    @classmethod
    def format_arg(cls, k, v=NoArgVal):
        key = cls.format_key(k)
        if v is True or v is NoArgVal:
            return key
        if v is False or v is None:
            return ''
        if not isinstance(v, (list, tuple, set)):
            v = [v]
        return [key] + [cls.format_value(x) for x in v]

    @classmethod
    def format_key(cls, k):
        return '{}{}'.format(cls.long_opt if len(k) > 1 else cls.short_opt, k)


class SacredArgument(FireArgument):
    prefix = 'with'
    kw_fmt = '{key}={value}'

    @classmethod
    def format_arg(cls, k, v=NoArgVal):
        if v is NoArgVal:
            return cls.format_value(k)
        return cls.kw_fmt.format(key=k, value=cls.format_value(v))

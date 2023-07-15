import pprint

from .adaptable_schemas import Bool, OROperator, Patch, Ref
from .attribute import Attribute
from .dict_schema import Dict
from .exceptions import ResolverError
from .integer_schema import Int
from .string_schema import Str


def convert_schema(spec):
    t = spec.pop('type')
    name = spec.pop('name')
    if t in ('int', 'integer'):
        return Int(name, **spec)
    elif t in ('str', 'string'):
        return Str(name, **spec)
    elif t in ('bool', 'boolean'):
        return Bool(name, **spec)
    elif t == 'dict':
        return Dict(name, *spec.get('args', []), **spec.get('kwargs', {}))
    raise ValueError(f'Unknown type: {t}')


def resolver(schemas, obj):
    if not isinstance(obj, dict) or not all(k in obj for k in ('keys', 'get_attr', 'has_key')):
        return

    for schema_type in filter(obj['has_key'], obj['keys']):
        new_params = []
        schema_obj = obj['get_attr'](schema_type)
        for p in schema_obj:
            if isinstance(p, (Patch, Ref, Attribute, OROperator)):
                resolved = p if p.resolved else p.resolve(schemas)
                new_params.append(resolved)
            else:
                raise ResolverError(f'Invalid parameter definition {p}')

        # FIXME: for some reason assigning params (f.accepts = new_params) does not work
        schema_obj.clear()
        schema_obj.extend(new_params)


def resolve_methods(schemas, to_resolve):
    while len(to_resolve) > 0:
        resolved = 0
        errors = []
        for method in list(to_resolve):
            try:
                resolver(schemas, method)
            except ResolverError as e:
                errors.append((method, e))
            else:
                to_resolve.remove(method)
                resolved += 1
        if resolved == 0:
            raise ValueError(f'Not all schemas could be resolved:\n{pprint.pformat(errors)}')

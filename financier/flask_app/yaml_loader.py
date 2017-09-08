from yaml.constructor import ConstructorError


def no_duplicates_constructor(loader, node, deep=False):
    """Check for duplicate keys."""

    mapping = {}
    duplicates = []
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        value = loader.construct_object(value_node, deep=deep)
        if key in mapping:
            # # Trying to correct and allow duplicates...failed so far
            # if key[-1] in digits:
            #     key = key[:-1] + str((int(key[-1]) + 1))
            # else:
            #     key = key + '1'
            duplicates.append(key)
        mapping[key] = value
    if len(duplicates) > 0:
        raise ConstructorError("while constructing a mapping", node.start_mark,
                               "found duplicate key (%s)" % ','.join(duplicates))
    return loader.construct_mapping(node, deep)

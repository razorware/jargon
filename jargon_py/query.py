import types


def get_nodes(collection, key):
    results = filter(lambda r: r.name == key, collection)

    for k, n in results:
        yield n


def first(iterator):
    """
    Returns the first occurrence from collection iterator

    :param iterator:

    :return:
    """
    item = None

    for i in iterator:
        item = i
        break

    return item


def child_tags(collection):
    if isinstance(collection, types.GeneratorType):
        collection = list(collection)[0].nodes

    return [n.name for n in collection]


def one(iterator):
    """
    Returns one instance found in the collection; raises exception if more than one are found

    :param iterator:

    :return:
    """
    item = None

    for i in iterator:
        if item is not None:
            raise Exception("expected only one instance but multiple exist")

        item = i
        break

    return item

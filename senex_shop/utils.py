from .models import OptionGroup, Option, split_option_unique_id


def get_all_options(obj, ids_only=False):
    sublist = []
    masterlist = []
    #Create a list of all the options & create all combos of the options
    for opt in obj.option_group.select_related().all():
        for value in opt.option_set.all().order_by('ordering'):
            if ids_only:
                sublist.append(value.unique_id)
            else:
                sublist.append(value)
        masterlist.append(sublist)
        sublist = []
    results = cross_list(masterlist)
    return results


def cross_list(sequences):
    result = [[]]
    for seq in sequences:
        result = [sublist + [item] for sublist in result for item in seq]
    return result


def serialize_options(product, selected_options=()):
    """
    Return a list of optiongroups and options for display to the customer.
    Only returns options that are actually used by members of this product.

    Return Value:
    [
    {
    name: 'group name',
    id: 'group id',
    items: [{
        name: 'opt name',
        value: 'opt value',
        price_change: 'opt price',
        selected: False,
        },{..}]
    },
    {..}
    ]

    Note: This doesn't handle the case where you have multiple options and
    some combinations aren't available. For example, you have option_groups
    color and size, and you have a yellow/large, a yellow/small, and a
    white/small, but you have no white/large - the customer will still see
    the options white and large.
    """
    all_options = product.get_valid_options()
    group_sortmap = OptionGroup.objects.get_sortmap()

    # first get all objects
    # right now we only have a list of option.unique_ids, and there are
    # probably a lot of dupes, so first list them uniquely
    values = []

    if all_options != [[]]:
        vals = {}
        groups = {}
        opts = {}
        serialized = {}
        for options in all_options:
            for option in options:
                if not opts.has_key(option):
                    k, v = split_option_unique_id(option)
                    vals[v] = False
                    groups[k] = False
                    opts[option] = None

        for option in Option.objects.filter(option_group__id__in=groups.keys(), value__in=vals.keys()):
            uid = option.unique_id
            if opts.has_key(uid):
                opts[uid] = option

        # now we have all the objects in our "opts" dictionary, so build the serialization dict

        for option in opts.values():
            if not serialized.has_key(option.option_group_id):
                serialized[option.option_group.id] = {
                    'name': option.option_group.name,
                    'description': option.option_group.description,
                    'id': option.option_group.id,
                    'items': [],
                }
            if not option in serialized[option.option_group_id]['items']:
                serialized[option.option_group_id]['items'] += [option]
                option.selected = option.unique_id in selected_options

        # first sort the option groups
        for k, v in serialized.items():
            values.append((group_sortmap[k], v))

        if values:
            values.sort()
            values = zip(*values)[1]

        #now go back and make sure option items are sorted properly.
        for v in values:
            v['items'] = _sort_options(v['items'])

    #log.debug('Serialized Options %s: %s', product.product.slug, values)
    return values


def _sort_options(lst):
    work = [(opt.ordering, opt) for opt in lst]
    work.sort()
    return zip(*work)[1]

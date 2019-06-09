def group_by(lst, key_selector):
    result = {}

    for elem in lst:
        key = key_selector(elem)

        if key not in result.keys():
            result[key] = []

        result[key].append(elem)

    return result

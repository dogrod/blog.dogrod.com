from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """
    Convert underscore case name to camelcase
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data:
            data = recursive_key_map(underscore_to_camelcase, data)

        return super(CustomJSONRenderer, self).render(
            data, accepted_media_type=None, renderer_context=None)


def underscore_to_camelcase(word, lower_first=True):
    """
    Convert underscore styled word to camelcase
    :param word:
    :param lower_first:
    :return:
    """
    result = ''.join(char.capitalize() for char in word.split('_'))
    if lower_first:
        return result[0].lower() + result[1:]
    else:
        return result


def recursive_key_map(method, data):
    """
    Recursive key-map object
    :param method:
    :param data:
    :return:
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if isinstance(key, str):
                key = method(key)
            new_dict[key] = recursive_key_map(method, value)
        return new_dict
    if hasattr(data, '__iter__') and not isinstance(data, str):
        return [recursive_key_map(method, value) for value in data]
    else:
        return data
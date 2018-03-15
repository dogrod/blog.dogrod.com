from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type, renderer_context):
        response = renderer_context['response']
        ret = super(CustomJSONRenderer, self).render(
            data, accepted_media_type=None, renderer_context=None)

        if hasattr(response.data, 'code'):
            return ret

        return """{{
            "code": {},
            "result": {}
        }}""".format(0, ret.decode()).encode()

from rest_framework.renderers import JSONRenderer


class JSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        final_data = {
            'success': True,
            'message': '',
            'errors': None,
            'data': None
        }
        if renderer_context['response'].exception:
            final_data['errors'] = data
            final_data['success'] = False
        else:
            try:
                detail = data.pop('detail', '')
            except (TypeError, AttributeError):
                detail = None

            if detail:
                final_data['message'] = detail

            if data or isinstance(data, list):
                final_data['data'] = data

        return super().render(
            final_data, accepted_media_type=accepted_media_type,
            renderer_context=renderer_context)

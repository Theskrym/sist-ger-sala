from django.forms import widgets
from django.utils.html import format_html

class ImageMapWidget(widgets.Widget):
    template_name = 'admin/image_map_widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        if value:
            x, y = value.split(',') if ',' in value else (0, 0)
        else:
            x, y = 0, 0
            
        return format_html(
            '<div class="image-map-widget">'
            '<img src="{}" class="floor-plan-image" data-x="{}" data-y="{}">'
            '<input type="hidden" name="{}_x" value="{}">'
            '<input type="hidden" name="{}_y" value="{}">'
            '</div>',
            attrs.get('image_url', ''),
            x, y,
            name, x,
            name, y
        )
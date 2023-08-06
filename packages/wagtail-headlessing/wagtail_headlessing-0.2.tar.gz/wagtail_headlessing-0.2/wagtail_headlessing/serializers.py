from rest_framework.fields import Field


class ChildPagesSerializer(Field):

    def to_representation(self, child_pages):
        return [{
            'id': child.id,
            'type': '%s.%s' % (child.specific_class._meta.app_label, child.specific_class.__name__),
            'slug': child.slug,
            'title': child.title
        } for child in child_pages]



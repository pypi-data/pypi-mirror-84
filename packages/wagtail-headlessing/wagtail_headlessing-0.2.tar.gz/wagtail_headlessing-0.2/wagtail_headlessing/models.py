from django.db import models
from wagtail.core.models import Page

# Create your models here.
class VuePage(Page):
    vue_template = 'pages/home_page.html'

    created = models.DateField(auto_now_add=True, auto_now=False)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previewing = False

    def set_previewing(self):
        self.previewing = True

    def get_template(self, *args, **kwargs):
        if self.vue_template:
            return self.vue_template

        return super().get_template()

    @property
    def get_child_pages(self):

        children = self.get_children().public().live()

        if self.previewing:
            children = [child.get_latest_revision_as_page() for child in children]

        return children
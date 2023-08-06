import re
from datetime import datetime
from django.core.exceptions import MultipleObjectsReturned
from django.urls import path, reverse
from django.http.response import Http404
from wagtail.api.v2.views import PagesAPIViewSet, parse_fields_parameter, BadRequestError
from wagtail.core.models import Page

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


slug_chain_item = re.compile(r'slug\d+')

class RootAPIViewSet(PagesAPIViewSet):

    def get_queryset(self):
        self.load_root_page()

        return self.root_page_model.objects.filter(id=self.root_page.id).public().live()

    def get_object(self):
        self.load_root_page()

        return self.root_page_model.objects.filter(id=self.root_page.id).public().live()[0]

    def load_root_page(self):
        if not hasattr(self, 'root_page_model'):
            self.root_page = self.get_root_page()
            self.root_page_model = type(self.root_page.specific)

    def listing_view(self, request):
        root_page = self.get_object()
        serializer = self.get_serializer(root_page)
        return Response(serializer.data)

class ExtendedPagesAPIViewSet(PagesAPIViewSet):
    """
    Our custom Pages API endpoint that allows finding pages by pk or slug
    """

    def get_serializer_class(self, model=None):

        request = self.request

        if not model:
            # Get model
            if self.action == 'listing_view':
                model = self.get_queryset().model
            else:
                model = type(self.get_object())

        # Fields
        if 'fields' in request.GET:
            try:
                fields_config = parse_fields_parameter(request.GET['fields'])
            except ValueError as e:
                raise BadRequestError("fields error: %s" % str(e))
        else:
            # Use default fields
            fields_config = []

        # Allow "detail_only" (eg parent) fields on detail view
        if self.action == 'listing_view':
            show_details = False
        else:
            show_details = True

        return self._get_serializer_class(self.request.wagtailapi_router, model, fields_config, show_details=show_details)


    def detail_view(self, request, pk):
        instance = self.load_specific(self.get_object())

        serialilzer_class = self.get_serializer_class(type(instance))
        serializer = serialilzer_class(instance)

        serializer = self.get_serializer(instance.specific)
        return Response(serializer.data)

    def load_specific(self, page_instance):
        return page_instance.specific

    def detail_slug_view(self, request, *args, **kwargs):
        slug_keys = [slug_key for slug_key in kwargs.keys() if slug_chain_item.match(slug_key)]
        slug_keys.sort()
        slug_chain = list(filter(None, [kwargs.get(slug_key) for slug_key in slug_keys]))
        kwargs = {}

        root = self.get_root_page()
        instance = root

        try:
            for slug in slug_chain:
                instance = instance.get_children().get(slug=slug)
        except Page.DoesNotExist:
            raise(Http404("Page not found"))

        instance = self.load_specific(instance)

        serialilzer_class = self.get_serializer_class(type(instance))
        kwargs['context'] = self.get_serializer_context()
        serializer = serialilzer_class(instance, *args, **kwargs)

        return Response(serializer.data)

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """

        def slug_chain_paths(max_depth=10):

            return [
                path(
                    ''.join(['<slug:slug%d>/' % slug_level for slug_level in range(n_levels)]),
                     cls.as_view({'get': 'detail_slug_view'}), name='detail_slug'
                ) for n_levels in range(max_depth)
            ]

        return [
            path('', cls.as_view({'get': 'listing_view'}), name='listing'),
            path('<int:pk>/', cls.as_view({'get': 'detail_view'}), name='detail'),
            path('find/', cls.as_view({'get': 'find_view'}), name='find'),
        ] + slug_chain_paths()


class ExtendedPagesPreviewAPIViewSet(ExtendedPagesAPIViewSet):

    permission_classes = [IsAuthenticated]

    meta_fields = ExtendedPagesAPIViewSet.meta_fields + [
        'latest_revision_created_at',
    ]

    def load_specific(self, page_instance):

        instance = page_instance.specific.get_latest_revision_as_page()
        instance.set_previewing()

        return instance

    def detail_view(self, request, pk):

        instance = self.load_specific(self.get_object())
        latest_revision_created_at = self.request.query_params.get('latest_revision_timestamp')

        if latest_revision_created_at:
            latest_revision_created_at = datetime.strptime(latest_revision_created_at, "%Y-%m-%dT%H:%M:%S.%f%z")

            if latest_revision_created_at == instance.latest_revision_created_at:
                return Response(None)

        serialilzer_class = self.get_serializer_class(type(instance))
        serializer = serialilzer_class(instance)

        serializer = self.get_serializer(instance.specific)

        return Response(serializer.data)

    def listing_view(self, request):
        queryset = self.get_queryset()
        self.check_query_parameters(queryset)
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        fake_queryset = [self.load_specific(instance) for instance in queryset]
        serializer = self.get_serializer(fake_queryset, many=True)

        return self.get_paginated_response(serializer.data)

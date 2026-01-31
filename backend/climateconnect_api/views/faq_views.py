from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from climateconnect_api.models.faq import FaqQuestion
from climateconnect_api.serializers.faq import FaqQuestionSerializer

# FAQ content changes infrequently - cache for 1 hour
FAQ_CACHE_TIMEOUT = getattr(settings, "FAQ_CACHE_TIMEOUT", 3600)


class ListFaqView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FaqQuestionSerializer

    @method_decorator(cache_page(FAQ_CACHE_TIMEOUT, key_prefix="faq_list"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return FaqQuestion.objects.select_related("section").all()


class AboutFaqView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FaqQuestionSerializer

    @method_decorator(cache_page(FAQ_CACHE_TIMEOUT, key_prefix="faq_about"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return FaqQuestion.objects.select_related("section").filter(section__is_on_about_page=True)

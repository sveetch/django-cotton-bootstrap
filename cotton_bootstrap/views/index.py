from django.conf import settings
from django.views.generic.base import RedirectView


class IndexView(RedirectView):
    """
    Index view is just a (non permanent) redirection to the first enabled component
    from settings.
    """
    permanent = False
    query_string = True
    pattern_name = "cotton_bootstrap:component-{}".format(
        list(settings.ENABLED_COMPONENT_DEMOS.keys())[0]
    )

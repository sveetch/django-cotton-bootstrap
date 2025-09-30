from django.urls import path
from django.conf import settings

from .views import IndexView, ComponentView


app_name = "cotton_bootstrap"


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
] + [
    path(
        "{}/".format(name),
        ComponentView.as_view(component_name=name),
        name="component-{}".format(name)
    )
    for name in settings.ENABLED_COMPONENT_DEMOS
]

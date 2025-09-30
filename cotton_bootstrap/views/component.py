from django.conf import settings
from django.views.generic.base import TemplateView


class ComponentView(TemplateView):
    """
    View for a component showcase.
    """
    # The name as defined in setting 'ENABLED_COMPONENT_DEMOS'
    component_name = None
    # Template name is automatically composed from 'component_name' value.
    template_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Name of current component
        context["BOOTSTRAP_COTTON_CURRENT_NAME"] = self.component_name
        # Current component data
        context["BOOTSTRAP_COTTON_CURRENT_COMPONENT"] = (
            settings.ENABLED_COMPONENT_DEMOS[self.component_name]
        )
        # Payload for some useful Bootstrap data
        context["BOOTSTRAP_COTTON_CONTEXT"] = settings.BOOTSTRAP_CONTEXT
        # Rebuild data to include view urlname to ease links in templates
        context["ENABLED_COMPONENT_DEMOS"] = {
            k: {
                "urlname": "cotton_bootstrap:component-{}".format(k),
                **v
            }
            for k, v in settings.ENABLED_COMPONENT_DEMOS.items()
        }

        return context

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response() is overridden.
        """
        if not self.component_name:
            raise ImproperlyConfigured(
                "ComponentView requires a definition of 'component_name'"
            )
        else:
            return "cotton_bootstrap/components/{}.html".format(self.component_name)

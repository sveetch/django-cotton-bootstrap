from django.urls import reverse

from cotton_bootstrap.utils.tests import html_pyquery


def test_index(client, settings):
    """
    Index should be a redirection to the first enabled component.
    """
    component_name = list(settings.ENABLED_COMPONENT_DEMOS.keys())[0]
    urlname = "cotton_bootstrap:component-{}".format(component_name)
    response = client.get("/", follow=True)

    assert response.redirect_chain == [
        (reverse(urlname), 302)
    ]
    assert response.status_code == 200

    dom = html_pyquery(response)
    content = dom.find(".page-title h1")[0].text

    assert content == settings.ENABLED_COMPONENT_DEMOS[component_name]["title"]


def test_component(client, settings):
    """
    Component view should respond with success and include its title.
    """
    for component_name, component_data in settings.ENABLED_COMPONENT_DEMOS.items():
        urlname = "cotton_bootstrap:component-{}".format(component_name)
        response = client.get(reverse(urlname), follow=True)

        assert response.redirect_chain == []
        assert response.status_code == 200

        dom = html_pyquery(response)
        content = dom.find(".page-title h1")[0].text

        assert content == component_data["title"]

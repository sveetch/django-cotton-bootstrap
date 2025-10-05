import bs4

from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.filters import VisibleWhitespaceFilter
from pygments.formatters import HtmlFormatter

from pyquery import PyQuery as pq

from django import template
from django.conf import settings
from django.utils.text import slugify

from django_cotton.cotton_loader import Loader as CottonLoader

register = template.Library()


def prettify_html(content, escape=False):
    """
    Parse given HTML content to prettify it with proper indentation then escape
    chevron characters so it is not interpreted as HTML.

    This is especially useful to present some HTML code.
    """
    pretty = bs4.BeautifulSoup(content, "html.parser").prettify(
        formatter=bs4.formatter.HTMLFormatter(
            entity_substitution=bs4.dammit.EntitySubstitution.substitute_html5,
            void_element_close_prefix="",
            empty_attributes_are_booleans=True,
            indent=4
        )
    )

    if escape:
        return pretty.replace("<", "&lt;").replace(">", "&gt;")

    return pretty


def highlight_html_filter(source, linenos=False, linenostart=1, identifier=None,
                          spaceless_safe=True):
    """
    Filter function to highlight HTML source with Pygments and some options.

    Line breaks are replaced with character ``↩`` to improve readability.

    This does not embed Pygments styles as inline styles, you will need to
    load these stylesheets from your document.

    Example:
        {{ "<p>Foobar</p>"|highlight_html }}
        {{ "<p>Foobar</p>"|highlight_html(linenos=True) }}
        {{ "<p>Foobar</p>"|highlight_html(linenos=True, linenostart=42) }}
        {{ "<p>Foobar</p>"|highlight_html(linenos=True, identifier="foo") }}

    Arguments:
        source (string): Source string to highlight.

    Keyword Arguments:
        linenos (bool): To enable or disable line numbers. Disabled by default.
        linenostart (int): To start line numbers from a specific number.
            Default to 1.
        identifier (string): An identifier string to prefix line anchors. So
            with ``id="foo"``, line 42 anchor will be named ``foo-42``. You
            must fill it to enable line anchor.
        spaceless_safe (boolean): Enable some options to enforce consistent elements
            for whitespaces so it is not stripped when a template use
            ``{% spaceless %}...{% endspaceless %}`` on top of content. This is
            enabled on default.

    Returns:
        string: HTML for highlighted source.
    """
    if linenos:
        linenos = "table"

    opts = {
        "cssclass": "highlight",
        "linenos": linenos,
        "linenostart": linenostart,
        "wrapcode": True,
    }
    if linenos and identifier:
        opts.update({
            "lineanchors": identifier,
            "anchorlinenos": True,
        })

    lexer = HtmlLexer()

    if spaceless_safe:
        lexer.add_filter(VisibleWhitespaceFilter(spaces="&nbsp;"))
        opts.update({
            "lineseparator": "<br>",
        })

    return highlight(source, lexer, HtmlFormatter(**opts))


def render_compiled_cotton(content, context=None):
    """
    Compile given content with Cotton compiler.
    """
    context = context or {}
    compiled = CottonLoader(engine=None).cotton_compiler.process(content)

    return template.Template(compiled).render(template.Context(context))


class ComponentDemoNode(template.Node):
    """
    Build HTML render of 'component_demo' templatetag.
    """
    def __init__(self, nodelist, options={}):
        self.nodelist = nodelist
        self.options = options

        self.defaults = {
            "template": getattr(
                settings,
                "COTTON_DEMO_TAG",
                "cotton_bootstrap/tags/demo.html"
            ),
            "with_render": True,
            "with_source": True,
            "with_escaped_source": True,
            "with_escaped_render": True,
        }

    def render(self, context):
        # Render passed source content
        source = self.nodelist.render(context)
        # Then render it with cotton
        rendered = render_compiled_cotton(source, context=context)

        # Resolve and append options from tag arguments
        opt_kwargs = {
            **self.defaults,
            **{
                key: val.resolve(context)
                for key, val in self.options.items()
            }
        }

        # Get template
        tag_template = template.loader.get_template(opt_kwargs["template"])

        # Render HTML
        return render_compiled_cotton(
            tag_template.template.source,
            context=template.Context({
                **opt_kwargs,
                "source": source,
                "rendered": rendered,
                "escaped_source": prettify_html(source, escape=True),
                "escaped_render": prettify_html(rendered, escape=True),
                "pygmented_source": highlight_html_filter(
                    prettify_html(source),
                    linenos=False
                ),
                "pygmented_render": highlight_html_filter(
                    prettify_html(rendered),
                    linenos=False
                ),
            })
        )


class DiscoverMenuNode(template.Node):
    """
    Build HTML render of 'discover_menu' templatetag.
    """
    def __init__(self, nodelist, options={}):
        self.nodelist = nodelist
        self.options = options

        self.defaults = {
            "template": getattr(
                settings,
                "COTTON_MENU_TAG",
                "cotton_bootstrap/tags/discover-menu.html"
            ),
        }

    def render(self, context):
        # Render passed content
        source = self.nodelist.render(context)

        # Resolve and append options from tag arguments
        opt_kwargs = {
            **self.defaults,
            **{
                key: val.resolve(context)
                for key, val in self.options.items()
            }
        }

        # Get template
        menu_template = template.loader.get_template(opt_kwargs["template"])
        # Get HTML query to find titles
        html_query = ".demo-part-title"

        # Render HTML
        return menu_template.render({
            **opt_kwargs,
            "source": source,
            "parts": [
                {"title": name.text, "slug": slugify(name.text)}
                for name in pq(source, parser="html").find(html_query)
            ],
        })


@register.filter(name="prettify_html")
def do_prettify_html(content):
    """
    Parse given HTML to prettify it with proper indentation and optionally escape
    chevron characters so it is not interpreted as HTML.
    """
    return prettify_html(content)


@register.tag(name="component_demo")
def do_component_demo(parser, token):
    """
    Cotton component demo templatetag parser.

    Usage sample: ::

        {% component_demo [template="cotton_bootstrap/tags/demo.html"] [with_render=True] [with_escaped_source=True] [with_escaped_render=True] %}
            {% cotton_verbatim %}
                <c-thecomponent />
            {% endcotton_verbatim %}
        {% endcomponent_demo %}

    From this sample you can see the supported options arguments. However you can also
    pass any other arguments, they are not implemented for usage in the default
    template but they are still available if you need.

    Default template can be defined from setting ``COTTON_DEMO_TAG`` and will default
    to ``component_demo/tag.html`` if setting does not exist.

    .. Warning::
        Because Cotton compiler happen before Django template, it is required to always
        surround content with ``{% cotton_verbatim %}....{% endcotton_verbatim %}``.
        Else Cotton will compile component code before it is sent to the template tag
        which is done to work on uncompiled source only.

    On default the shipped templatetag template will display the rendered HTML, the
    escaped source and the escaped rendered HTML.

    .. Note::
        This templatetag is done to support fully Cotton so its own template can use
        Cotton components.
    """  # noqa
    bits = token.split_contents()
    remaining_bits = bits[1:]
    options = template.base.token_kwargs(remaining_bits, parser)

    nodelist = parser.parse(("endcomponent_demo",))
    parser.delete_first_token()

    return ComponentDemoNode(
        nodelist,
        options=options
    )


@register.tag(name="discover_menu")
def do_discover_menu(parser, token):
    """
    Parse content to find titles used to build contextual navigation.

    Usage sample: ::

        {% discover_menu [template="cotton_bootstrap/tags/discover-menu.html"] %}
            ...
        {% enddiscover_menu %}

    """  # noqa
    bits = token.split_contents()
    remaining_bits = bits[1:]
    options = template.base.token_kwargs(remaining_bits, parser)

    nodelist = parser.parse(("enddiscover_menu",))
    parser.delete_first_token()

    return DiscoverMenuNode(
        nodelist,
        options=options
    )

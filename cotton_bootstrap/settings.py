"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

"""
ENABLED_COMPONENT_DEMOS = {
    "buttons": {"title": "Buttons"},
    "flexgrid": {"title": "Flex grid"},
    "card": {"title": "Card"},
    "listgroup": {"title": "List group"},
}

BOOTSTRAP_CONTEXT = {
    "button_variants": [
        "primary",
        "secondary",
        "success",
        "danger",
        "warning",
        "info",
        "light",
        "dark",
        "link",
    ],
}
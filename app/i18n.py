from flask_babel import gettext, LazyString



class CustomLazyString(LazyString):
    """Subclass compatible with Dash views."""

    def to_plotly_json(self):
        return str(self)


def lazy_gettext(string, **variables):
    """Use this for strings in dash components."""
    return CustomLazyString(gettext, string, **variables)


def gettext_noop(string):
    return string

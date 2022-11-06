import bleach

ALLOWED_TAGS = [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'div', 'blockquote', 'q'
]


def escape_html(text, tags=None):
    if tags is None:
        tags = ALLOWED_TAGS
    return bleach.clean(text, tags=tags)

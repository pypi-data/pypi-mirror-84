from webencodings import UTF8, decode, lookup

from .parser import parse_stylesheet


def decode_stylesheet_bytes(css_bytes, protocol_encoding=None,
                            environment_encoding=None):
    """Determine the character encoding of a CSS stylesheet and decode it.

    This is based on the presence of a :abbr:`BOM (Byte Order Mark)`,
    a ``@charset`` rule, and encoding meta-information.

    :type css_bytes: :obj:`bytes`
    :param css_bytes: A CSS byte string.
    :type protocol_encoding: :obj:`str`
    :param protocol_encoding:
        The encoding label, if any, defined by HTTP or equivalent protocol.
        (e.g. via the ``charset`` parameter of the ``Content-Type`` header.)
    :type environment_encoding: :class:`webencodings.Encoding`
    :param environment_encoding:
        The `environment encoding
        <https://www.w3.org/TR/css-syntax/#environment-encoding>`_, if any.
    :returns:
        A 2-tuple of a decoded Unicode string and the
        :class:`webencodings.Encoding` object that was used.

    """
    # https://drafts.csswg.org/css-syntax/#the-input-byte-stream
    if protocol_encoding:
        fallback = lookup(protocol_encoding)
        if fallback:
            return decode(css_bytes, fallback)
    if css_bytes.startswith(b'@charset "'):
        # 10 is len(b'@charset "')
        # 100 is arbitrary so that no encoding label is more than 100-10 bytes.
        end_quote = css_bytes.find(b'"', 10, 100)
        if end_quote != -1 and css_bytes.startswith(b'";', end_quote):
            fallback = lookup(css_bytes[10:end_quote].decode('latin1'))
            if fallback:
                if fallback.name in ('utf-16be', 'utf-16le'):
                    return decode(css_bytes, UTF8)
                return decode(css_bytes, fallback)
    if environment_encoding:
        return decode(css_bytes, environment_encoding)
    return decode(css_bytes, UTF8)


def parse_stylesheet_bytes(css_bytes, protocol_encoding=None,
                           environment_encoding=None,
                           skip_comments=False, skip_whitespace=False):
    """Parse :diagram:`stylesheet` from bytes,
    determining the character encoding as web browsers do.

    This is used when reading a file or fetching a URL.
    The character encoding is determined from the initial bytes
    (a :abbr:`BOM (Byte Order Mark)` or a ``@charset`` rule)
    as well as the parameters. The ultimate fallback is UTF-8.

    :type css_bytes: :obj:`bytes`
    :param css_bytes: A CSS byte string.
    :type protocol_encoding: :obj:`str`
    :param protocol_encoding:
        The encoding label, if any, defined by HTTP or equivalent protocol.
        (e.g. via the ``charset`` parameter of the ``Content-Type`` header.)
    :type environment_encoding: :class:`webencodings.Encoding`
    :param environment_encoding:
        The `environment encoding`_, if any.
    :type skip_comments: :obj:`bool`
    :param skip_comments:
        Ignore CSS comments at the top-level of the stylesheet.
        If the input is a string, ignore all comments.
    :type skip_whitespace: :obj:`bool`
    :param skip_whitespace:
        Ignore whitespace at the top-level of the stylesheet.
        Whitespace is still preserved
        in the :attr:`~tinycss2.ast.QualifiedRule.prelude`
        and the :attr:`~tinycss2.ast.QualifiedRule.content` of rules.
    :returns:
        A ``(rules, encoding)`` tuple.

        * ``rules`` is a list of
          :class:`~tinycss2.ast.QualifiedRule`,
          :class:`~tinycss2.ast.AtRule`,
          :class:`~tinycss2.ast.Comment` (if ``skip_comments`` is false),
          :class:`~tinycss2.ast.WhitespaceToken`
          (if ``skip_whitespace`` is false),
          and :class:`~tinycss2.ast.ParseError` objects.
        * ``encoding`` is the :class:`webencodings.Encoding` object
          that was used.
          If ``rules`` contains an ``@import`` rule, this is
          the `environment encoding`_ for the imported stylesheet.

    .. _environment encoding:
            https://www.w3.org/TR/css-syntax/#environment-encoding

    .. code-block:: python

        response = urlopen('http://example.net/foo.css')
        rules, encoding = parse_stylesheet_bytes(
            css_bytes=response.read(),
            # Python 3.x
            protocol_encoding=response.info().get_content_type().get_param('charset'),
            # Python 2.x
            protocol_encoding=response.info().gettype().getparam('charset'),
        )
        for rule in rules:
            ...

    """
    css_unicode, encoding = decode_stylesheet_bytes(
        css_bytes, protocol_encoding, environment_encoding)
    stylesheet = parse_stylesheet(css_unicode, skip_comments, skip_whitespace)
    return stylesheet, encoding

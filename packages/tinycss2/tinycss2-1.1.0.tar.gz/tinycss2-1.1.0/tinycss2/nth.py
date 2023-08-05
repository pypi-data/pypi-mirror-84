import re

from .parser import _next_significant, _to_token_iterator


def parse_nth(input):
    """Parse `<An+B> <https://drafts.csswg.org/css-syntax-3/#anb>`_,
    as found in `:nth-child()
    <https://drafts.csswg.org/selectors/#nth-child-pseudo>`_
    and related Selector pseudo-classes.

    Although tinycss2 does not include a full Selector parser,
    this bit of syntax is included as it is particularly tricky to define
    on top of a CSS tokenizer.

    :type input: :obj:`str` or :term:`iterable`
    :param input: A string or an iterable of :term:`component values`.
    :returns:
        A ``(a, b)`` tuple of integers, or :obj:`None` if the input is invalid.

    """
    tokens = _to_token_iterator(input, skip_comments=True)
    token = _next_significant(tokens)
    if token is None:
        return
    token_type = token.type
    if token_type == 'number' and token.is_integer:
        return parse_end(tokens, 0, token.int_value)
    elif token_type == 'dimension' and token.is_integer:
        unit = token.lower_unit
        if unit == 'n':
            return parse_b(tokens, token.int_value)
        elif unit == 'n-':
            return parse_signless_b(tokens, token.int_value, -1)
        else:
            match = N_DASH_DIGITS_RE.match(unit)
            if match:
                return parse_end(tokens, token.int_value, int(match.group(1)))
    elif token_type == 'ident':
        ident = token.lower_value
        if ident == 'even':
            return parse_end(tokens, 2, 0)
        elif ident == 'odd':
            return parse_end(tokens, 2, 1)
        elif ident == 'n':
            return parse_b(tokens, 1)
        elif ident == '-n':
            return parse_b(tokens, -1)
        elif ident == 'n-':
            return parse_signless_b(tokens, 1, -1)
        elif ident == '-n-':
            return parse_signless_b(tokens, -1, -1)
        elif ident[0] == '-':
            match = N_DASH_DIGITS_RE.match(ident[1:])
            if match:
                return parse_end(tokens, -1, int(match.group(1)))
        else:
            match = N_DASH_DIGITS_RE.match(ident)
            if match:
                return parse_end(tokens, 1, int(match.group(1)))
    elif token == '+':
        token = next(tokens)  # Whitespace after an initial '+' is invalid.
        if token.type == 'ident':
            ident = token.lower_value
            if ident == 'n':
                return parse_b(tokens, 1)
            elif ident == 'n-':
                return parse_signless_b(tokens, 1, -1)
            else:
                match = N_DASH_DIGITS_RE.match(ident)
                if match:
                    return parse_end(tokens, 1, int(match.group(1)))


def parse_b(tokens, a):
    token = _next_significant(tokens)
    if token is None:
        return (a, 0)
    elif token == '+':
        return parse_signless_b(tokens, a, 1)
    elif token == '-':
        return parse_signless_b(tokens, a, -1)
    elif (token.type == 'number' and token.is_integer and
          token.representation[0] in '-+'):
        return parse_end(tokens, a, token.int_value)


def parse_signless_b(tokens, a, b_sign):
    token = _next_significant(tokens)
    if (token.type == 'number' and token.is_integer and
            not token.representation[0] in '-+'):
        return parse_end(tokens, a, b_sign * token.int_value)


def parse_end(tokens, a, b):
    if _next_significant(tokens) is None:
        return (a, b)


N_DASH_DIGITS_RE = re.compile('^n(-[0-9]+)$')

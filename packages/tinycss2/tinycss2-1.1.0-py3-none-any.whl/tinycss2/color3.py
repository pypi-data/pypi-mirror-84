import collections
import re
from colorsys import hls_to_rgb

from .parser import parse_one_component_value


class RGBA(collections.namedtuple('RGBA', ['red', 'green', 'blue', 'alpha'])):
    """An RGBA color.

    A tuple of four floats in the 0..1 range: ``(red, green, blue, alpha)``.

    .. attribute:: red

        Convenience access to the red channel. Same as ``rgba[0]``.

    .. attribute:: green

        Convenience access to the green channel. Same as ``rgba[1]``.

    .. attribute:: blue

        Convenience access to the blue channel. Same as ``rgba[2]``.

    .. attribute:: alpha

        Convenience access to the alpha channel. Same as ``rgba[3]``.

    """


def parse_color(input):
    """Parse a color value as defined in `CSS Color Level 3
    <https://www.w3.org/TR/css-color-3/>`_.

    :type input: :obj:`str` or :term:`iterable`
    :param input: A string or an iterable of :term:`component values`.
    :returns:
        * :obj:`None` if the input is not a valid color value.
          (No exception is raised.)
        * The string ``'currentColor'`` for the ``currentColor`` keyword
        * Or a :class:`RGBA` object for every other values
          (including keywords, HSL and HSLA.)
          The alpha channel is clipped to [0, 1]
          but red, green, or blue can be out of range
          (eg. ``rgb(-10%, 120%, 0%)`` is represented as
          ``(-0.1, 1.2, 0, 1)``.)

    """
    if isinstance(input, str):
        token = parse_one_component_value(input, skip_comments=True)
    else:
        token = input
    if token.type == 'ident':
        return _COLOR_KEYWORDS.get(token.lower_value)
    elif token.type == 'hash':
        for multiplier, regexp in _HASH_REGEXPS:
            match = regexp(token.value)
            if match:
                channels = [
                    int(group * multiplier, 16) / 255
                    for group in match.groups()]
                if len(channels) == 3:
                    channels.append(1.)
                return RGBA(*channels)
    elif token.type == 'function':
        args = _parse_comma_separated(token.arguments)
        if args:
            name = token.lower_name
            if name == 'rgb':
                return _parse_rgb(args, alpha=1.)
            elif name == 'rgba':
                alpha = _parse_alpha(args[3:])
                if alpha is not None:
                    return _parse_rgb(args[:3], alpha)
            elif name == 'hsl':
                return _parse_hsl(args, alpha=1.)
            elif name == 'hsla':
                alpha = _parse_alpha(args[3:])
                if alpha is not None:
                    return _parse_hsl(args[:3], alpha)


def _parse_alpha(args):
    """Parse a list of one alpha value.

    If args is a list of a single INTEGER or NUMBER token,
    return its value clipped to the 0..1 range. Otherwise, return None.

    """
    if len(args) == 1 and args[0].type == 'number':
        return min(1, max(0, args[0].value))


def _parse_rgb(args, alpha):
    """Parse a list of RGB channels.

    If args is a list of 3 INTEGER tokens or 3 PERCENTAGE tokens, return RGB
    values as a tuple of 3 floats in 0..1. Otherwise, return None.

    """
    types = [arg.type for arg in args]
    if (types == ['number', 'number', 'number'] and
            all(a.is_integer for a in args)):
        r, g, b = [arg.int_value / 255 for arg in args[:3]]
        return RGBA(r, g, b, alpha)
    elif types == ['percentage', 'percentage', 'percentage']:
        r, g, b = [arg.value / 100 for arg in args[:3]]
        return RGBA(r, g, b, alpha)


def _parse_hsl(args, alpha):
    """Parse a list of HSL channels.

    If args is a list of 1 INTEGER token and 2 PERCENTAGE tokens, return RGB
    values as a tuple of 3 floats in 0..1. Otherwise, return None.

    """
    types = [arg.type for arg in args]
    if types == ['number', 'percentage', 'percentage'] and args[0].is_integer:
        r, g, b = hls_to_rgb(
            args[0].int_value / 360, args[2].value / 100, args[1].value / 100)
        return RGBA(r, g, b, alpha)


def _parse_comma_separated(tokens):
    """Parse a list of tokens (typically the content of a function token)
    as arguments made of a single token each, separated by mandatory commas,
    with optional white space around each argument.

    return the argument list without commas or white space;
    or None if the function token content do not match the description above.

    """
    tokens = [token for token in tokens
              if token.type not in ('whitespace', 'comment')]
    if not tokens:
        return []
    if len(tokens) % 2 == 1 and all(token == ',' for token in tokens[1::2]):
        return tokens[::2]


_HASH_REGEXPS = (
    (2, re.compile('^{}$'.format(4 * '([\\da-f])'), re.I).match),
    (1, re.compile('^{}$'.format(4 * '([\\da-f]{2})'), re.I).match),
    (2, re.compile('^{}$'.format(3 * '([\\da-f])'), re.I).match),
    (1, re.compile('^{}$'.format(3 * '([\\da-f]{2})'), re.I).match),
)


# (r, g, b) in 0..255
_BASIC_COLOR_KEYWORDS = [
    ('black', (0, 0, 0)),
    ('silver', (192, 192, 192)),
    ('gray', (128, 128, 128)),
    ('white', (255, 255, 255)),
    ('maroon', (128, 0, 0)),
    ('red', (255, 0, 0)),
    ('purple', (128, 0, 128)),
    ('fuchsia', (255, 0, 255)),
    ('green', (0, 128, 0)),
    ('lime', (0, 255, 0)),
    ('olive', (128, 128, 0)),
    ('yellow', (255, 255, 0)),
    ('navy', (0, 0, 128)),
    ('blue', (0, 0, 255)),
    ('teal', (0, 128, 128)),
    ('aqua', (0, 255, 255)),
]


# (r, g, b) in 0..255
_EXTENDED_COLOR_KEYWORDS = [
    ('aliceblue', (240, 248, 255)),
    ('antiquewhite', (250, 235, 215)),
    ('aqua', (0, 255, 255)),
    ('aquamarine', (127, 255, 212)),
    ('azure', (240, 255, 255)),
    ('beige', (245, 245, 220)),
    ('bisque', (255, 228, 196)),
    ('black', (0, 0, 0)),
    ('blanchedalmond', (255, 235, 205)),
    ('blue', (0, 0, 255)),
    ('blueviolet', (138, 43, 226)),
    ('brown', (165, 42, 42)),
    ('burlywood', (222, 184, 135)),
    ('cadetblue', (95, 158, 160)),
    ('chartreuse', (127, 255, 0)),
    ('chocolate', (210, 105, 30)),
    ('coral', (255, 127, 80)),
    ('cornflowerblue', (100, 149, 237)),
    ('cornsilk', (255, 248, 220)),
    ('crimson', (220, 20, 60)),
    ('cyan', (0, 255, 255)),
    ('darkblue', (0, 0, 139)),
    ('darkcyan', (0, 139, 139)),
    ('darkgoldenrod', (184, 134, 11)),
    ('darkgray', (169, 169, 169)),
    ('darkgreen', (0, 100, 0)),
    ('darkgrey', (169, 169, 169)),
    ('darkkhaki', (189, 183, 107)),
    ('darkmagenta', (139, 0, 139)),
    ('darkolivegreen', (85, 107, 47)),
    ('darkorange', (255, 140, 0)),
    ('darkorchid', (153, 50, 204)),
    ('darkred', (139, 0, 0)),
    ('darksalmon', (233, 150, 122)),
    ('darkseagreen', (143, 188, 143)),
    ('darkslateblue', (72, 61, 139)),
    ('darkslategray', (47, 79, 79)),
    ('darkslategrey', (47, 79, 79)),
    ('darkturquoise', (0, 206, 209)),
    ('darkviolet', (148, 0, 211)),
    ('deeppink', (255, 20, 147)),
    ('deepskyblue', (0, 191, 255)),
    ('dimgray', (105, 105, 105)),
    ('dimgrey', (105, 105, 105)),
    ('dodgerblue', (30, 144, 255)),
    ('firebrick', (178, 34, 34)),
    ('floralwhite', (255, 250, 240)),
    ('forestgreen', (34, 139, 34)),
    ('fuchsia', (255, 0, 255)),
    ('gainsboro', (220, 220, 220)),
    ('ghostwhite', (248, 248, 255)),
    ('gold', (255, 215, 0)),
    ('goldenrod', (218, 165, 32)),
    ('gray', (128, 128, 128)),
    ('green', (0, 128, 0)),
    ('greenyellow', (173, 255, 47)),
    ('grey', (128, 128, 128)),
    ('honeydew', (240, 255, 240)),
    ('hotpink', (255, 105, 180)),
    ('indianred', (205, 92, 92)),
    ('indigo', (75, 0, 130)),
    ('ivory', (255, 255, 240)),
    ('khaki', (240, 230, 140)),
    ('lavender', (230, 230, 250)),
    ('lavenderblush', (255, 240, 245)),
    ('lawngreen', (124, 252, 0)),
    ('lemonchiffon', (255, 250, 205)),
    ('lightblue', (173, 216, 230)),
    ('lightcoral', (240, 128, 128)),
    ('lightcyan', (224, 255, 255)),
    ('lightgoldenrodyellow', (250, 250, 210)),
    ('lightgray', (211, 211, 211)),
    ('lightgreen', (144, 238, 144)),
    ('lightgrey', (211, 211, 211)),
    ('lightpink', (255, 182, 193)),
    ('lightsalmon', (255, 160, 122)),
    ('lightseagreen', (32, 178, 170)),
    ('lightskyblue', (135, 206, 250)),
    ('lightslategray', (119, 136, 153)),
    ('lightslategrey', (119, 136, 153)),
    ('lightsteelblue', (176, 196, 222)),
    ('lightyellow', (255, 255, 224)),
    ('lime', (0, 255, 0)),
    ('limegreen', (50, 205, 50)),
    ('linen', (250, 240, 230)),
    ('magenta', (255, 0, 255)),
    ('maroon', (128, 0, 0)),
    ('mediumaquamarine', (102, 205, 170)),
    ('mediumblue', (0, 0, 205)),
    ('mediumorchid', (186, 85, 211)),
    ('mediumpurple', (147, 112, 219)),
    ('mediumseagreen', (60, 179, 113)),
    ('mediumslateblue', (123, 104, 238)),
    ('mediumspringgreen', (0, 250, 154)),
    ('mediumturquoise', (72, 209, 204)),
    ('mediumvioletred', (199, 21, 133)),
    ('midnightblue', (25, 25, 112)),
    ('mintcream', (245, 255, 250)),
    ('mistyrose', (255, 228, 225)),
    ('moccasin', (255, 228, 181)),
    ('navajowhite', (255, 222, 173)),
    ('navy', (0, 0, 128)),
    ('oldlace', (253, 245, 230)),
    ('olive', (128, 128, 0)),
    ('olivedrab', (107, 142, 35)),
    ('orange', (255, 165, 0)),
    ('orangered', (255, 69, 0)),
    ('orchid', (218, 112, 214)),
    ('palegoldenrod', (238, 232, 170)),
    ('palegreen', (152, 251, 152)),
    ('paleturquoise', (175, 238, 238)),
    ('palevioletred', (219, 112, 147)),
    ('papayawhip', (255, 239, 213)),
    ('peachpuff', (255, 218, 185)),
    ('peru', (205, 133, 63)),
    ('pink', (255, 192, 203)),
    ('plum', (221, 160, 221)),
    ('powderblue', (176, 224, 230)),
    ('purple', (128, 0, 128)),
    ('red', (255, 0, 0)),
    ('rosybrown', (188, 143, 143)),
    ('royalblue', (65, 105, 225)),
    ('saddlebrown', (139, 69, 19)),
    ('salmon', (250, 128, 114)),
    ('sandybrown', (244, 164, 96)),
    ('seagreen', (46, 139, 87)),
    ('seashell', (255, 245, 238)),
    ('sienna', (160, 82, 45)),
    ('silver', (192, 192, 192)),
    ('skyblue', (135, 206, 235)),
    ('slateblue', (106, 90, 205)),
    ('slategray', (112, 128, 144)),
    ('slategrey', (112, 128, 144)),
    ('snow', (255, 250, 250)),
    ('springgreen', (0, 255, 127)),
    ('steelblue', (70, 130, 180)),
    ('tan', (210, 180, 140)),
    ('teal', (0, 128, 128)),
    ('thistle', (216, 191, 216)),
    ('tomato', (255, 99, 71)),
    ('turquoise', (64, 224, 208)),
    ('violet', (238, 130, 238)),
    ('wheat', (245, 222, 179)),
    ('white', (255, 255, 255)),
    ('whitesmoke', (245, 245, 245)),
    ('yellow', (255, 255, 0)),
    ('yellowgreen', (154, 205, 50)),
]


# (r, g, b, a) in 0..1 or a string marker
_SPECIAL_COLOR_KEYWORDS = {
    'currentcolor': 'currentColor',
    'transparent': RGBA(0., 0., 0., 0.),
}


# RGBA namedtuples of (r, g, b, a) in 0..1 or a string marker
_COLOR_KEYWORDS = _SPECIAL_COLOR_KEYWORDS.copy()
_COLOR_KEYWORDS.update(
    # 255 maps to 1, 0 to 0, the rest is linear.
    (keyword, RGBA(r / 255., g / 255., b / 255., 1.))
    for keyword, (r, g, b) in _BASIC_COLOR_KEYWORDS + _EXTENDED_COLOR_KEYWORDS)

"""
    cairocffi.test_pixbuf
    ~~~~~~~~~~~~~~~~~~~~~

    Test suite for cairocffi.pixbuf.

    :copyright: Copyright 2013-2019 by Simon Sapin
    :license: BSD, see LICENSE for details.

"""

import base64
import sys
import zlib

import pytest

from . import constants, pixbuf

PNG_BYTES = base64.b64decode(
    b'iVBORw0KGgoAAAANSUhEUgAAAAMAAAACCAYAAACddGYaAAAAE0lEQV'
    b'QI12NkaPjfwAAFTAxIAAAuNwIDqJbDRgAAAABJRU5ErkJggg==')

JPEG_BYTES = zlib.decompress(base64.b64decode(
    b'eJylzb0JgFAMBOA704hYvIC9oygIou7nPFq4g3+Nm0RT+iy9VPkIF9vsQhjavgVJdM/ATjS'
    b'+/YqX/O2gzdAUCUSoSJSitAUFiHdS1xArXBlr5qrf2wO58HkiigrlWK+T7TezChqU'))


def test_api():
    with pytest.raises(pixbuf.ImageLoadingError):
        pixbuf.decode_to_image_surface(b'')
    with pytest.raises(pixbuf.ImageLoadingError):
        pixbuf.decode_to_image_surface(b'Not a valid image.')
    with pytest.raises(pixbuf.ImageLoadingError):
        pixbuf.decode_to_image_surface(PNG_BYTES[:10])
    surface, format_name = pixbuf.decode_to_image_surface(PNG_BYTES)
    assert format_name == 'png'
    assert_decoded(surface)


def test_gdk():
    if pixbuf.gdk is None:
        pytest.xfail()
    pixbuf_obj, format_name = pixbuf.decode_to_pixbuf(PNG_BYTES)
    assert format_name == 'png'
    assert_decoded(pixbuf.pixbuf_to_cairo_gdk(pixbuf_obj))


def test_slices():
    pixbuf_obj, format_name = pixbuf.decode_to_pixbuf(PNG_BYTES)
    assert format_name == 'png'
    assert_decoded(pixbuf.pixbuf_to_cairo_png(pixbuf_obj))


def test_size():
    pixbuf_obj, format_name = pixbuf.decode_to_pixbuf(PNG_BYTES, 10, 10)
    assert format_name == 'png'
    surface = pixbuf.pixbuf_to_cairo_png(pixbuf_obj)
    assert surface.get_width() == 10
    assert surface.get_height() == 10
    assert surface.get_format() == constants.FORMAT_ARGB32


def test_png():
    pixbuf_obj, format_name = pixbuf.decode_to_pixbuf(JPEG_BYTES)
    assert format_name == 'jpeg'
    assert_decoded(pixbuf.pixbuf_to_cairo_slices(pixbuf_obj),
                   constants.FORMAT_RGB24, b'\xff\x00\x80\xff')


def assert_decoded(surface, format_=constants.FORMAT_ARGB32,
                   rgba=b'\x80\x00\x40\x80'):
    assert surface.get_width() == 3
    assert surface.get_height() == 2
    assert surface.get_format() == format_
    if sys.byteorder == 'little':  # pragma: no cover
        rgba = rgba[::-1]
    assert surface.get_data()[:] == rgba * 6

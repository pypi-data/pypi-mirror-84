"""
    cairocffi.matrix
    ~~~~~~~~~~~~~~~~

    Transformation matrices.

    :copyright: Copyright 2013-2019 by Simon Sapin
    :license: BSD, see LICENSE for details.

"""

from . import _check_status, cairo, ffi


class Matrix(object):
    """A 2D transformation matrix.

    Matrices are used throughout cairo to convert between
    different coordinate spaces.
    A :class:`Matrix` holds an affine transformation,
    such as a scale, rotation, shear, or a combination of these.
    The transformation of a point (x,y) is given by::

        x_new = xx * x + xy * y + x0
        y_new = yx * x + yy * y + y0

    The current transformation matrix of a :class:`Context`,
    represented as a :class:`Matrix`,
    defines the transformation from user-space coordinates
    to device-space coordinates.
    See :meth:`Context.get_matrix` and :meth:`Context.set_matrix`.

    The default values produce an identity matrix.

    Matrices can be compared with ``m1 == m2`` and ``m2 != m2``
    as well as multiplied with ``m3 = m1 * m2``.

    """
    def __init__(self, xx=1, yx=0, xy=0, yy=1, x0=0, y0=0):
        self._pointer = ffi.new('cairo_matrix_t *')
        cairo.cairo_matrix_init(self._pointer, xx, yx, xy, yy, x0, y0)

    @classmethod
    def init_rotate(cls, radians):
        """Return a new :class:`Matrix` for a transformation
        that rotates by :obj:`radians`.

        :type radians: float
        :param radians:
            Angle of rotation, in radians.
            The direction of rotation is defined such that
            positive angles rotate in the direction
            from the positive X axis toward the positive Y axis.
            With the default axis orientation of cairo,
            positive angles rotate in a clockwise direction.

        """
        result = cls()
        cairo.cairo_matrix_init_rotate(result._pointer, radians)
        return result

    def as_tuple(self):
        """Return all of the matrix’s components.

        :returns: A ``(xx, yx, xy, yy, x0, y0)`` tuple of floats.

        """
        ptr = self._pointer
        return (ptr.xx, ptr.yx, ptr.xy, ptr.yy, ptr.x0, ptr.y0)

    def copy(self):
        """Return a new copy of this matrix."""
        return type(self)(*self.as_tuple())

    def __getitem__(self, index):
        return getattr(
            self._pointer, ('xx', 'yx', 'xy', 'yy', 'x0', 'y0')[index])

    def __iter__(self):
        return iter(self.as_tuple())

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __ne__(self, other):
        return self.as_tuple() != other.as_tuple()

    def __repr__(self):
        class_ = type(self)
        return '%s(%g, %g, %g, %g, %g, %g)' % (
            (class_.__name__,) + self.as_tuple())

    def multiply(self, other):
        """Multiply with another matrix
        and return the result as a new :class:`Matrix` object.
        Same as ``self * other``.

        """
        res = Matrix()
        cairo.cairo_matrix_multiply(
            res._pointer, self._pointer, other._pointer)
        return res

    __mul__ = multiply

    def translate(self, tx, ty):
        """Applies a translation by :obj:`tx`, :obj:`ty`
        to the transformation in this matrix.

        The effect of the new transformation is to
        first translate the coordinates by :obj:`tx` and :obj:`ty`,
        then apply the original transformation to the coordinates.

        .. note::
            This changes the matrix in-place.

        :param tx: Amount to translate in the X direction.
        :param ty: Amount to translate in the Y direction.
        :type tx: float
        :type ty: float

        """
        cairo.cairo_matrix_translate(self._pointer, tx, ty)

    def scale(self, sx, sy=None):
        """Applies scaling by :obj:`sx`, :obj:`sy`
        to the transformation in this matrix.

        The effect of the new transformation is to
        first scale the coordinates by :obj:`sx` and :obj:`sy`,
        then apply the original transformation to the coordinates.

        If :obj:`sy` is omitted, it is the same as :obj:`sx`
        so that scaling preserves aspect ratios.

        .. note::
            This changes the matrix in-place.

        :param sx: Scale factor in the X direction.
        :param sy: Scale factor in the Y direction.
        :type sx: float
        :type sy: float

        """
        if sy is None:
            sy = sx
        cairo.cairo_matrix_scale(self._pointer, sx, sy)

    def rotate(self, radians):
        """Applies a rotation by :obj:`radians`
        to the transformation in this matrix.

        The effect of the new transformation is to
        first rotate the coordinates by :obj:`radians`,
        then apply the original transformation to the coordinates.

        .. note::
            This changes the matrix in-place.

        :type radians: float
        :param radians:
            Angle of rotation, in radians.
            The direction of rotation is defined such that positive angles
            rotate in the direction from the positive X axis
            toward the positive Y axis.
            With the default axis orientation of cairo,
            positive angles rotate in a clockwise direction.

        """
        cairo.cairo_matrix_rotate(self._pointer, radians)

    def invert(self):
        """Changes matrix to be the inverse of its original value.
        Not all transformation matrices have inverses;
        if the matrix collapses points together (it is degenerate),
        then it has no inverse and this function will fail.

        .. note::
            This changes the matrix in-place.

        :raises: :exc:`CairoError` on degenerate matrices.

        """
        _check_status(cairo.cairo_matrix_invert(self._pointer))

    def inverted(self):
        """Return the inverse of this matrix. See :meth:`invert`.

        :raises: :exc:`CairoError` on degenerate matrices.
        :returns: A new :class:`Matrix` object.

        """
        matrix = self.copy()
        matrix.invert()
        return matrix

    def transform_point(self, x, y):
        """Transforms the point ``(x, y)`` by this matrix.

        :param x: X position.
        :param y: Y position.
        :type x: float
        :type y: float
        :returns: A ``(new_x, new_y)`` tuple of floats.

        """
        xy = ffi.new('double[2]', [x, y])
        cairo.cairo_matrix_transform_point(self._pointer, xy + 0, xy + 1)
        return tuple(xy)

    def transform_distance(self, dx, dy):
        """Transforms the distance vector ``(dx, dy)`` by this matrix.
        This is similar to :meth:`transform_point`
        except that the translation components of the transformation
        are ignored.
        The calculation of the returned vector is as follows::

            dx2 = dx1 * xx + dy1 * xy
            dy2 = dx1 * yx + dy1 * yy

        Affine transformations are position invariant,
        so the same vector always transforms to the same vector.
        If ``(x1, y1)`` transforms to ``(x2, y2)``
        then ``(x1 + dx1, y1 + dy1)`` will transform
        to ``(x1 + dx2, y1 + dy2)`` for all values of ``x1`` and ``x2``.

        :param dx: X component of a distance vector.
        :param dy: Y component of a distance vector.
        :type dx: float
        :type dy: float
        :returns: A ``(new_dx, new_dy)`` tuple of floats.

        """
        xy = ffi.new('double[2]', [dx, dy])
        cairo.cairo_matrix_transform_distance(self._pointer, xy + 0, xy + 1)
        return tuple(xy)

    def _component_property(name):
        return property(
            lambda self: getattr(self._pointer, name),
            lambda self, value: setattr(self._pointer, name, value),
            doc='Read-write attribute access to a single float component.')

    xx = _component_property('xx')
    yx = _component_property('yx')
    xy = _component_property('xy')
    yy = _component_property('yy')
    x0 = _component_property('x0')
    y0 = _component_property('y0')
    del _component_property

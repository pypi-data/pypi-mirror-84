from tri_declarative import (
    dispatch,
    EMPTY,
)

from iommi.reinvokable import reinvokable


class Errors(set):
    @dispatch(
        attrs=EMPTY,
    )
    @reinvokable
    def __init__(self, *, parent, attrs, errors=None, template=None):
        super(Errors, self).__init__(errors or [])
        self._parent = parent
        self.attrs = attrs
        self.template = template
        self.iommi_style = None

    def __str__(self):
        return self.__html__()

    def __bool__(self):
        return len(self) != 0

    def __html__(self):
        if not self:
            return ''

        from iommi import Fragment
        return Fragment(
            _name='error',
            tag='ul',
            attrs=self.attrs,
            template=self.template,
            children={
                f'error_{i}': Fragment(
                    tag='li',
                    children__text=error,
                )
                for i, error in enumerate(sorted(self))
            },
        ).bind(parent=self._parent).__html__()

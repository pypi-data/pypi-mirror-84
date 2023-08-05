from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SinkStageSpecifier


class IndexedPNGOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing indexed-PNG format
    image-segmentation annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image segmentation files in the indexed-PNG format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import ToIndexedPNG, IndexedPNGWriter
        return ToIndexedPNG, IndexedPNGWriter

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier

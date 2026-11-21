"""areaperimeter：面积与周长计算与练习单生成。"""

from .model import (
    Measurement,
    circle,
    composite_area,
    parallelogram,
    rectangle,
    square,
    trapezoid,
    triangle_area,
)
from .render import (
    circle_svg,
    formula_table,
    parallelogram_svg,
    rectangle_svg,
    trapezoid_svg,
    triangle_svg,
    worksheet_html,
)

__all__ = [
    "Measurement",
    "circle",
    "composite_area",
    "parallelogram",
    "rectangle",
    "square",
    "trapezoid",
    "triangle_area",
    "circle_svg",
    "formula_table",
    "parallelogram_svg",
    "rectangle_svg",
    "trapezoid_svg",
    "triangle_svg",
    "worksheet_html",
]

__version__ = "0.1.0"

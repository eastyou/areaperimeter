"""面积与周长计算：常见平面图形与组合图形。"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

ShapeValue = float


@dataclass(frozen=True)
class Measurement:
    """面积与周长结果，周长未知时保持 0。"""

    area: float
    perimeter: float = 0.0

    def rounded(self, digits: int = 2) -> "Measurement":
        return Measurement(round(self.area, digits), round(self.perimeter, digits))

    def as_dict(self) -> dict:
        data = {"area": round(self.area, 2)}
        if self.perimeter:
            data["perimeter"] = round(self.perimeter, 2)
        return data


def format_number(value: float) -> str:
    """去掉多余的小数零，方便命令行阅读。"""
    rounded = round(float(value), 2)
    if abs(rounded - round(rounded)) < 1e-9:
        return str(int(round(rounded)))
    return ("%.2f" % rounded).rstrip("0").rstrip(".")


def to_number(value: object, name: str) -> float:
    """把整数、浮点数或数字字符串转换成有限的浮点数。"""
    if isinstance(value, bool):
        raise TypeError("%s 不能是布尔值" % name)
    if isinstance(value, (int, float)):
        number = float(value)
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("%s 不能为空" % name)
        try:
            number = float(text)
        except ValueError:
            raise ValueError("%s 必须是数字，当前为 %r" % (name, value)) from None
    else:
        raise TypeError("%s 必须是数字" % name)
    if not math.isfinite(number):
        raise ValueError("%s 必须是有限数字" % name)
    return number


def positive(value: object, name: str) -> float:
    """校验并返回大于 0 的数值。"""
    number = to_number(value, name)
    if number <= 0:
        raise ValueError("%s 必须大于 0" % name)
    return number


def rectangle(width: ShapeValue, height: ShapeValue) -> Measurement:
    w = positive(width, "长")
    h = positive(height, "宽")
    return Measurement(w * h, 2 * (w + h))


def square(side: ShapeValue) -> Measurement:
    s = positive(side, "边长")
    return Measurement(s * s, 4 * s)


def triangle_area(base: ShapeValue, height: ShapeValue) -> float:
    b = positive(base, "底")
    h = positive(height, "高")
    return 0.5 * b * h


def circle(radius: ShapeValue) -> Measurement:
    r = positive(radius, "半径")
    return Measurement(math.pi * r * r, 2 * math.pi * r)


def parallelogram(
    base: ShapeValue, height: ShapeValue, side: ShapeValue
) -> Measurement:
    b = positive(base, "底")
    h = positive(height, "高")
    s = positive(side, "斜边")
    if s < h:
        raise ValueError("斜边不能小于高")
    return Measurement(b * h, 2 * (b + s))


def trapezoid(
    top: ShapeValue,
    bottom: ShapeValue,
    height: ShapeValue,
    left: ShapeValue,
    right: ShapeValue,
) -> Measurement:
    a = positive(top, "上底")
    b = positive(bottom, "下底")
    h = positive(height, "高")
    l = positive(left, "左腰")
    r = positive(right, "右腰")
    return Measurement(0.5 * (a + b) * h, a + b + l + r)


def composite_area(parts: Sequence[Tuple[ShapeValue, ShapeValue]]) -> float:
    """组合图形面积：把若干矩形面积相加。"""
    if not parts:
        raise ValueError("至少需要一个矩形")
    total = 0.0
    for index, (width, height) in enumerate(parts, start=1):
        total += rectangle(width, height).area
    return total


def describe(kind: str, result: Measurement) -> str:
    """生成中文结果描述，周长未知时只显示面积。"""
    labels = {
        "rectangle": "长方形",
        "square": "正方形",
        "circle": "圆",
        "parallelogram": "平行四边形",
        "trapezoid": "梯形",
    }
    name = labels.get(kind, kind)
    if result.perimeter:
        return "%s：面积 %s，周长 %s" % (
            name,
            format_number(result.area),
            format_number(result.perimeter),
        )
    return "%s：面积 %s" % (name, format_number(result.area))


def pick_perimeter(result: Optional[Measurement]) -> Optional[float]:
    """便于外部安全读取周长。"""
    if result is None or not result.perimeter:
        return None
    return result.perimeter

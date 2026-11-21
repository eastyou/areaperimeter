"""areaperimeter 核心逻辑测试。"""

import math
import unittest

from areaperimeter.model import (
    Measurement,
    circle,
    composite_area,
    describe,
    format_number,
    parallelogram,
    pick_perimeter,
    positive,
    rectangle,
    square,
    to_number,
    trapezoid,
    triangle_area,
)


class NumberTests(unittest.TestCase):
    def test_int(self):
        self.assertEqual(to_number(3, "长"), 3.0)

    def test_float(self):
        self.assertEqual(to_number(2.5, "长"), 2.5)

    def test_numeric_string(self):
        self.assertEqual(to_number(" 4.5 ", "长"), 4.5)

    def test_rejects_bool(self):
        with self.assertRaises(TypeError):
            to_number(True, "长")

    def test_rejects_empty_string(self):
        with self.assertRaises(ValueError):
            to_number("  ", "长")

    def test_rejects_text(self):
        with self.assertRaises(ValueError):
            to_number("abc", "长")

    def test_rejects_none(self):
        with self.assertRaises(TypeError):
            to_number(None, "长")  # type: ignore[arg-type]

    def test_rejects_infinity(self):
        with self.assertRaises(ValueError):
            to_number(float("inf"), "长")

    def test_rejects_nan(self):
        with self.assertRaises(ValueError):
            to_number(float("nan"), "长")

    def test_positive_accepts(self):
        self.assertEqual(positive("2", "边长"), 2.0)

    def test_positive_rejects_zero(self):
        with self.assertRaises(ValueError):
            positive(0, "边长")

    def test_positive_rejects_negative(self):
        with self.assertRaises(ValueError):
            positive(-3, "边长")


class FormatNumberTests(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(format_number(12.0), "12")

    def test_decimal(self):
        self.assertEqual(format_number(12.345), "12.35")

    def test_trailing_zero(self):
        self.assertEqual(format_number(12.5), "12.5")

    def test_small(self):
        self.assertEqual(format_number(0.1 + 0.2), "0.3")


class RectangleTests(unittest.TestCase):
    def test_area_and_perimeter(self):
        result = rectangle(8, 5)
        self.assertAlmostEqual(result.area, 40)
        self.assertAlmostEqual(result.perimeter, 26)

    def test_string_inputs(self):
        result = rectangle("6", "4")
        self.assertAlmostEqual(result.area, 24)

    def test_square(self):
        result = square(6)
        self.assertAlmostEqual(result.area, 36)
        self.assertAlmostEqual(result.perimeter, 24)

    def test_rejects_zero(self):
        with self.assertRaises(ValueError):
            rectangle(0, 5)

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            rectangle(8, -1)

    def test_rejects_text(self):
        with self.assertRaises(ValueError):
            rectangle("八", 5)  # type: ignore[arg-type]


class CircleTests(unittest.TestCase):
    def test_area(self):
        result = circle(3)
        self.assertAlmostEqual(result.area, math.pi * 9)

    def test_perimeter(self):
        result = circle(3)
        self.assertAlmostEqual(result.perimeter, 2 * math.pi * 3)

    def test_rejects_zero(self):
        with self.assertRaises(ValueError):
            circle(0)

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            circle(-2)


class TriangleTests(unittest.TestCase):
    def test_area(self):
        self.assertAlmostEqual(triangle_area(12, 7), 42)

    def test_decimal(self):
        self.assertAlmostEqual(triangle_area(2.5, 4), 5)

    def test_rejects_zero_base(self):
        with self.assertRaises(ValueError):
            triangle_area(0, 5)

    def test_rejects_negative_height(self):
        with self.assertRaises(ValueError):
            triangle_area(4, -2)


class ParallelogramTests(unittest.TestCase):
    def test_area_and_perimeter(self):
        result = parallelogram(9, 4, 5)
        self.assertAlmostEqual(result.area, 36)
        self.assertAlmostEqual(result.perimeter, 28)

    def test_rejects_side_shorter_than_height(self):
        with self.assertRaises(ValueError):
            parallelogram(9, 6, 5)

    def test_rejects_zero(self):
        with self.assertRaises(ValueError):
            parallelogram(0, 4, 5)


class TrapezoidTests(unittest.TestCase):
    def test_area_and_perimeter(self):
        result = trapezoid(4, 10, 6, 5, 5)
        self.assertAlmostEqual(result.area, 42)
        self.assertAlmostEqual(result.perimeter, 24)

    def test_rejects_zero_top(self):
        with self.assertRaises(ValueError):
            trapezoid(0, 10, 6, 5, 5)

    def test_rejects_negative_leg(self):
        with self.assertRaises(ValueError):
            trapezoid(4, 10, 6, -1, 5)


class CompositeTests(unittest.TestCase):
    def test_sum_of_rectangles(self):
        self.assertAlmostEqual(composite_area([(4, 3), (2, 5)]), 22)

    def test_single_part(self):
        self.assertAlmostEqual(composite_area([(4, 3)]), 12)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            composite_area([])

    def test_rejects_invalid_part(self):
        with self.assertRaises(ValueError):
            composite_area([(4, 3), (0, 5)])


class HelperTests(unittest.TestCase):
    def test_measurement_rounded(self):
        rounded = Measurement(12.3456, 7.8912).rounded()
        self.assertEqual(rounded.area, 12.35)
        self.assertEqual(rounded.perimeter, 7.89)

    def test_measurement_dict(self):
        data = rectangle(8, 5).as_dict()
        self.assertEqual(data, {"area": 40, "perimeter": 26})

    def test_measurement_dict_without_perimeter(self):
        self.assertEqual(Measurement(12).as_dict(), {"area": 12})

    def test_describe_with_perimeter(self):
        text = describe("rectangle", rectangle(8, 5))
        self.assertIn("长方形", text)
        self.assertIn("40", text)
        self.assertIn("26", text)

    def test_describe_without_perimeter(self):
        text = describe("circle", Measurement(28.27))
        self.assertIn("面积", text)
        self.assertNotIn("周长", text)

    def test_pick_perimeter(self):
        self.assertEqual(pick_perimeter(rectangle(4, 3)), 14)

    def test_pick_perimeter_none(self):
        self.assertIsNone(pick_perimeter(None))

    def test_pick_perimeter_zero(self):
        self.assertIsNone(pick_perimeter(Measurement(10)))


if __name__ == "__main__":
    unittest.main()

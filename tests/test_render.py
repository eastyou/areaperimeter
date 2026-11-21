"""areaperimeter 渲染测试。"""

import unittest

from areaperimeter.render import (
    circle_svg,
    formula_table,
    parallelogram_svg,
    rectangle_svg,
    trapezoid_svg,
    triangle_svg,
    worksheet_html,
)

ITEMS = [("长方形长 4、宽 3，求面积。", "面积 12"), ("圆的半径是 2。", "面积 12.57")]


class ShapeSvgTests(unittest.TestCase):
    def test_rectangle_svg(self):
        svg = rectangle_svg(8, 5)
        self.assertTrue(svg.startswith("<svg"))
        self.assertIn("长方形", svg)
        self.assertIn("</svg>", svg)

    def test_rectangle_shows_dimensions(self):
        svg = rectangle_svg(8, 5)
        self.assertIn(">8<", svg)
        self.assertIn(">5<", svg)

    def test_rectangle_rejects_invalid(self):
        with self.assertRaises(ValueError):
            rectangle_svg(0, 5)

    def test_circle_svg(self):
        svg = circle_svg(3)
        self.assertIn("<circle", svg)
        self.assertIn("r = 3", svg)

    def test_circle_rejects_invalid(self):
        with self.assertRaises(ValueError):
            circle_svg(-1)

    def test_triangle_svg(self):
        svg = triangle_svg(12, 7)
        self.assertIn("<polygon", svg)
        self.assertIn("底 12", svg)
        self.assertIn("高 7", svg)

    def test_triangle_rejects_invalid(self):
        with self.assertRaises(ValueError):
            triangle_svg(0, 7)

    def test_parallelogram_svg(self):
        svg = parallelogram_svg(9, 4, 5)
        self.assertIn("平行四边形", svg)
        self.assertIn("底 9", svg)

    def test_parallelogram_rejects_short_side(self):
        with self.assertRaises(ValueError):
            parallelogram_svg(9, 6, 5)

    def test_trapezoid_svg(self):
        svg = trapezoid_svg(4, 10, 6, 5, 5)
        self.assertIn("梯形", svg)
        self.assertIn("上底 4", svg)
        self.assertIn("下底 10", svg)

    def test_trapezoid_rejects_invalid(self):
        with self.assertRaises(ValueError):
            trapezoid_svg(0, 10, 6, 5, 5)


class TableTests(unittest.TestCase):
    def test_formula_table(self):
        table = formula_table()
        self.assertIn("<table>", table)
        self.assertIn("长方形", table)
        self.assertIn("梯形", table)

    def test_formula_table_has_circle(self):
        self.assertIn("π", formula_table())


class WorksheetTests(unittest.TestCase):
    def test_full_document(self):
        page = worksheet_html("练习", ITEMS)
        self.assertTrue(page.startswith("<!DOCTYPE html>"))
        self.assertIn("</html>", page)

    def test_contains_questions(self):
        page = worksheet_html("练习", ITEMS)
        self.assertIn("长方形长 4", page)

    def test_contains_answers(self):
        page = worksheet_html("练习", ITEMS)
        self.assertIn("参考答案", page)
        self.assertIn("面积 12", page)

    def test_contains_formula_table(self):
        page = worksheet_html("练习", ITEMS)
        self.assertIn("面积公式", page)

    def test_escapes_html(self):
        page = worksheet_html("<b>练习</b>", [("<i>题</i>", "<u>答</u>")])
        self.assertNotIn("<b>", page)
        self.assertNotIn("<i>", page)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            worksheet_html("练习", [])


if __name__ == "__main__":
    unittest.main()

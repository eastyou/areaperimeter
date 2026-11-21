"""areaperimeter 命令行测试。"""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from areaperimeter.cli import main


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class ShapeCommandTests(unittest.TestCase):
    def test_rectangle(self):
        code, out, _ = run(["rect", "8", "5"])
        self.assertEqual(code, 0)
        self.assertIn("面积 40", out)
        self.assertIn("周长 26", out)

    def test_square(self):
        code, out, _ = run(["square", "6"])
        self.assertEqual(code, 0)
        self.assertIn("面积 36", out)

    def test_circle(self):
        code, out, _ = run(["circle", "3"])
        self.assertEqual(code, 0)
        self.assertIn("面积", out)
        self.assertIn("周长", out)

    def test_triangle(self):
        code, out, _ = run(["tri", "12", "7"])
        self.assertEqual(code, 0)
        self.assertIn("面积 42", out)

    def test_parallelogram(self):
        code, out, _ = run(["para", "9", "4", "5"])
        self.assertEqual(code, 0)
        self.assertIn("面积 36", out)

    def test_trapezoid(self):
        code, out, _ = run(["trap", "4", "10", "6", "5", "5"])
        self.assertEqual(code, 0)
        self.assertIn("面积 42", out)

    def test_composite(self):
        code, out, _ = run(["composite", "4", "3", "2", "5"])
        self.assertEqual(code, 0)
        self.assertIn("面积 22", out)


class ErrorTests(unittest.TestCase):
    def test_negative_value(self):
        code, _, err = run(["rect", "-8", "5"])
        self.assertEqual(code, 2)
        self.assertIn("大于 0", err)

    def test_zero_value(self):
        code, _, err = run(["square", "0"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_bad_composite_pairs(self):
        code, _, err = run(["composite", "4", "3", "2"])
        self.assertEqual(code, 2)
        self.assertIn("成对", err)

    def test_short_side_parallelogram(self):
        code, _, err = run(["para", "9", "6", "5"])
        self.assertEqual(code, 2)
        self.assertIn("斜边", err)


class SheetCommandTests(unittest.TestCase):
    def test_sheet_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "sheet.html"
            code, out, _ = run(["sheet", "-o", str(output)])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            self.assertIn("已生成练习单", out)

    def test_sheet_contains_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "sheet.html"
            run(["sheet", "-o", str(output)])
            text = output.read_text(encoding="utf-8")
            self.assertIn("参考答案", text)

    def test_sheet_custom_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "sheet.html"
            run(["sheet", "-o", str(output), "--title", "六年级复习"])
            self.assertIn("六年级复习", output.read_text(encoding="utf-8"))

    def test_sheet_requires_output(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main(["sheet"])
        self.assertEqual(ctx.exception.code, 2)


class ParserTests(unittest.TestCase):
    def test_help(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stdout(io.StringIO()):
                main(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_no_command(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main([])
        self.assertEqual(ctx.exception.code, 2)

    def test_unknown_command(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main(["sphere"])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()

"""areaperimeter 命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from .model import (
    Measurement,
    circle,
    composite_area,
    format_number,
    parallelogram,
    rectangle,
    square,
    trapezoid,
    triangle_area,
)
from .render import circle_svg, rectangle_svg, triangle_svg, worksheet_html


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="areaperimeter", description="面积与周长：常见图形计算与练习单生成"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    rect = sub.add_parser("rect", help="长方形")
    rect.add_argument("width", type=float)
    rect.add_argument("height", type=float)

    sq = sub.add_parser("square", help="正方形")
    sq.add_argument("side", type=float)

    circ = sub.add_parser("circle", help="圆")
    circ.add_argument("radius", type=float)

    tri = sub.add_parser("tri", help="三角形面积")
    tri.add_argument("base", type=float)
    tri.add_argument("height", type=float)

    para = sub.add_parser("para", help="平行四边形")
    para.add_argument("base", type=float)
    para.add_argument("height", type=float)
    para.add_argument("side", type=float)

    trap = sub.add_parser("trap", help="梯形")
    trap.add_argument("top", type=float)
    trap.add_argument("bottom", type=float)
    trap.add_argument("height", type=float)
    trap.add_argument("left", type=float)
    trap.add_argument("right", type=float)

    comp = sub.add_parser("composite", help="组合图形面积（宽 高 成对输入）")
    comp.add_argument("parts", nargs="+", type=float)

    sheet = sub.add_parser("sheet", help="生成练习单")
    sheet.add_argument("-o", "--output", required=True)
    sheet.add_argument("--title", default="面积与周长练习")

    return parser


def _report_measurement(name: str, result: Measurement) -> None:
    print(
        "%s：面积 %s，周长 %s"
        % (name, format_number(result.area), format_number(result.perimeter))
    )


def _run(args: argparse.Namespace) -> int:
    if args.command == "rect":
        _report_measurement("长方形", rectangle(args.width, args.height))
        return 0
    if args.command == "square":
        _report_measurement("正方形", square(args.side))
        return 0
    if args.command == "circle":
        result = circle(args.radius)
        print(
            "圆：面积 %s，周长 %s"
            % (format_number(result.area), format_number(result.perimeter))
        )
        return 0
    if args.command == "tri":
        print("三角形：面积 %s" % format_number(triangle_area(args.base, args.height)))
        return 0
    if args.command == "para":
        _report_measurement(
            "平行四边形", parallelogram(args.base, args.height, args.side)
        )
        return 0
    if args.command == "trap":
        _report_measurement(
            "梯形",
            trapezoid(args.top, args.bottom, args.height, args.left, args.right),
        )
        return 0
    if args.command == "composite":
        if len(args.parts) % 2 != 0:
            raise ValueError("组合图形参数必须成对出现：宽 高 宽 高")
        pairs = list(zip(args.parts[0::2], args.parts[1::2]))
        print("组合图形：面积 %s" % format_number(composite_area(pairs)))
        return 0
    if args.command == "sheet":
        items = _sample_items()
        Path(args.output).write_text(worksheet_html(args.title, items), encoding="utf-8")
        print("已生成练习单：%s" % args.output)
        return 0
    raise ValueError("未知命令：%s" % args.command)


def _sample_items() -> List[Tuple[str, str]]:
    return [
        (
            "长方形长 8 厘米、宽 5 厘米，求面积和周长。",
            "面积 40 平方厘米，周长 26 厘米",
        ),
        (
            "正方形边长 6 分米，求面积和周长。",
            "面积 36 平方分米，周长 24 分米",
        ),
        (
            "三角形底 12 米、高 7 米，求面积。",
            "面积 42 平方米",
        ),
        (
            "平行四边形底 9 厘米、高 4 厘米、斜边 5 厘米，求面积和周长。",
            "面积 36 平方厘米，周长 28 厘米",
        ),
        (
            "梯形上底 4 米、下底 10 米、高 6 米、两腰各 5 米，求面积和周长。",
            "面积 42 平方米，周长 24 米",
        ),
        (
            "圆的半径是 3 厘米，求面积和周长（π 取 3.14）。",
            "面积约 28.26 平方厘米，周长约 18.84 厘米",
        ),
    ]


def _ensure_utf8_console() -> None:
    """Windows 控制台默认编码可能无法输出中文，尽量切换为 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            continue


def main(argv: Optional[Sequence[str]] = None) -> int:
    _ensure_utf8_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return _run(args)
    except (TypeError, ValueError) as exc:
        print("错误：%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

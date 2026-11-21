"""面积与周长的 SVG 图形和练习页渲染。"""

from __future__ import annotations

import html
import math
from typing import Dict, Sequence, Tuple

from .model import format_number, positive

WIDTH, HEIGHT, MARGIN = 360, 260, 48


def _safe(text: object) -> str:
    return html.escape(str(text), quote=True)


def _frame(label: str, body: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 260" '
        'role="img" aria-label="%s">\n'
        '<rect width="360" height="260" fill="#f8fafc"/>\n%s\n'
        '<text x="180" y="242" font-size="13" fill="#334155" '
        'text-anchor="middle">%s</text>\n</svg>' % (_safe(label), body, _safe(label))
    )


def _fit(width: float, height: float) -> float:
    return min((WIDTH - 2 * MARGIN) / width, (HEIGHT - 2 * MARGIN) / height)


def rectangle_svg(width: float, height: float) -> str:
    w = positive(width, "长")
    h = positive(height, "宽")
    scale = _fit(w, h)
    draw_w, draw_h = w * scale, h * scale
    x = (WIDTH - draw_w) / 2
    y = (HEIGHT - draw_h) / 2 - 6
    body = (
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#dbeafe" '
        'stroke="#2563eb" stroke-width="2"/>' % (x, y, draw_w, draw_h)
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#1e3a8a" text-anchor="middle">%s</text>'
        % (x + draw_w / 2, y + draw_h + 18, _safe(format_number(w)))
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#1e3a8a">%s</text>'
        % (x + draw_w + 6, y + draw_h / 2, _safe(format_number(h)))
    )
    return _frame("长方形", body)


def circle_svg(radius: float) -> str:
    r = positive(radius, "半径")
    scale = _fit(2 * r, 2 * r)
    draw_r = r * scale
    cx, cy = WIDTH / 2, (HEIGHT / 2) - 6
    body = (
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#dcfce7" stroke="#16a34a" '
        'stroke-width="2"/>' % (cx, cy, draw_r)
        + '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#166534"/>'
        % (cx, cy, cx + draw_r, cy)
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#166534">r = %s</text>'
        % (cx + draw_r / 2, cy - 6, _safe(format_number(r)))
    )
    return _frame("圆", body)


def triangle_svg(base: float, height: float) -> str:
    b = positive(base, "底")
    h = positive(height, "高")
    scale = _fit(b, h)
    draw_b, draw_h = b * scale, h * scale
    x = (WIDTH - draw_b) / 2
    bottom = (HEIGHT + draw_h) / 2 - 10
    top = bottom - draw_h
    apex = x + draw_b / 2
    body = (
        '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#fef3c7" '
        'stroke="#d97706" stroke-width="2"/>' % (apex, top, x, bottom, x + draw_b, bottom)
        + '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#b45309" '
        'stroke-dasharray="4 4"/>' % (apex, top, apex, bottom)
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#92400e" text-anchor="middle">底 %s</text>'
        % (x + draw_b / 2, bottom + 18, _safe(format_number(b)))
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#92400e">高 %s</text>'
        % (apex + 6, top + draw_h / 2, _safe(format_number(h)))
    )
    return _frame("三角形", body)


def parallelogram_svg(base: float, height: float, side: float) -> str:
    b = positive(base, "底")
    h = positive(height, "高")
    s = positive(side, "斜边")
    if s < h:
        raise ValueError("斜边不能小于高")
    slant = math.sqrt(s * s - h * h)
    scale = _fit(b + slant, h)
    draw_b, draw_h, draw_slant = b * scale, h * scale, slant * scale
    x = (WIDTH - draw_b - draw_slant) / 2
    bottom = (HEIGHT + draw_h) / 2 - 10
    top = bottom - draw_h
    points = (
        "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f"
        % (
            x + draw_slant,
            top,
            x + draw_slant + draw_b,
            top,
            x + draw_b,
            bottom,
            x,
            bottom,
        )
    )
    body = (
        '<polygon points="%s" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>'
        % points
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#5b21b6" text-anchor="middle">底 %s</text>'
        % (x + draw_b / 2 + draw_slant / 2, bottom + 18, _safe(format_number(b)))
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#5b21b6">高 %s</text>'
        % (x + draw_b + 6, top + draw_h / 2, _safe(format_number(h)))
    )
    return _frame("平行四边形", body)


def trapezoid_svg(
    top: float, bottom: float, height: float, left: float, right: float
) -> str:
    a = positive(top, "上底")
    b = positive(bottom, "下底")
    h = positive(height, "高")
    positive(left, "左腰")
    positive(right, "右腰")
    scale = _fit(b, h)
    draw_a, draw_b, draw_h = a * scale, b * scale, h * scale
    x = (WIDTH - draw_b) / 2
    base_y = (HEIGHT + draw_h) / 2 - 10
    top_y = base_y - draw_h
    top_x = x + (draw_b - draw_a) / 2
    points = (
        "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f"
        % (top_x, top_y, top_x + draw_a, top_y, x + draw_b, base_y, x, base_y)
    )
    body = (
        '<polygon points="%s" fill="#ffe4e6" stroke="#e11d48" stroke-width="2"/>'
        % points
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#9f1239" text-anchor="middle">上底 %s</text>'
        % (top_x + draw_a / 2, top_y - 8, _safe(format_number(a)))
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#9f1239" text-anchor="middle">下底 %s</text>'
        % (x + draw_b / 2, base_y + 18, _safe(format_number(b)))
        + '<text x="%.1f" y="%.1f" font-size="12" fill="#9f1239">高 %s</text>'
        % (x + draw_b + 6, top_y + draw_h / 2, _safe(format_number(h)))
    )
    return _frame("梯形", body)


def formula_table() -> str:
    rows = [
        ("长方形", "面积 = 长 × 宽", "周长 = (长 + 宽) × 2"),
        ("正方形", "面积 = 边长 × 边长", "周长 = 边长 × 4"),
        ("三角形", "面积 = 底 × 高 ÷ 2", "周长 = 三边之和"),
        ("平行四边形", "面积 = 底 × 高", "周长 = (底 + 斜边) × 2"),
        ("梯形", "面积 = (上底 + 下底) × 高 ÷ 2", "周长 = 四边之和"),
        ("圆", "面积 = π × 半径²", "周长 = 2 × π × 半径"),
    ]
    body = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (_safe(a), _safe(b), _safe(c))
        for a, b, c in rows
    )
    return (
        "<table><thead><tr><th>图形</th><th>面积公式</th><th>周长公式</th></tr>"
        "</thead><tbody>%s</tbody></table>" % body
    )


def worksheet_html(
    title: str, items: Sequence[Tuple[str, str]]
) -> str:
    """生成题目页与答案页合并的练习单。"""
    if not items:
        raise ValueError("至少需要一道题目")
    safe_title = _safe(title or "面积与周长练习")
    questions = "".join(
        '<li><span class="q">%s</span><span class="line"></span></li>' % _safe(question)
        for question, _ in items
    )
    answers = "".join(
        "<li>%d. %s</li>" % (index, _safe(answer))
        for index, (_, answer) in enumerate(items, start=1)
    )
    return (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>%s</title>\n<style>\n"
        "body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;"
        "background:#f1f5f9;margin:0;padding:24px;color:#0f172a}\n"
        ".card{max-width:760px;margin:0 auto 20px;background:#fff;border-radius:16px;"
        "padding:24px;box-shadow:0 10px 24px rgba(15,23,42,.1)}\n"
        "h1{font-size:21px;margin:0 0 12px}h2{font-size:16px;margin:18px 0 8px}\n"
        "ol{padding-left:22px;line-height:2.2}li{margin-bottom:6px}\n"
        ".line{display:inline-block;width:210px;border-bottom:1px dashed #94a3b8;"
        "margin-left:10px}\n"
        "table{width:100%%;border-collapse:collapse;font-size:14px}\n"
        "th,td{border-bottom:1px solid #e2e8f0;padding:8px;text-align:left}\n"
        "footer{font-size:12px;color:#64748b;margin-top:14px}\n"
        "</style>\n</head>\n<body>\n"
        "<section class=\"card\"><h1>%s</h1>%s<h2>题目</h2><ol>%s</ol>"
        "<footer>由 areaperimeter 生成 · 结果保留两位小数</footer></section>\n"
        "<section class=\"card\"><h2>参考答案</h2><ol>%s</ol></section>\n"
        "</body>\n</html>"
        % (safe_title, safe_title, formula_table(), questions, answers)
    )

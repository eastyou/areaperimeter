# areaperimeter

[![CI](https://github.com/eastyou/areaperimeter/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/areaperimeter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

面积与周长计算工具：长方形、正方形、三角形、平行四边形、梯形、圆，附带 SVG 图示和练习单。

## 功能

- 常见平面图形的面积与周长计算
- 组合图形面积（多个矩形相加）
- 参数校验：非数字、零、负数、无穷大都会给出中文提示
- 生成带尺寸标注的 SVG 图形
- 生成含公式表、题目页和答案页的练习单
- 结果保留两位小数并自动去掉多余零

## 安装

```bash
pip install -e .
```

也可以直接运行 `python -m areaperimeter`。

## 使用

```bash
areaperimeter rect 8 5          # 面积 40，周长 26
areaperimeter square 6          # 面积 36，周长 24
areaperimeter circle 3          # 面积 28.27，周长 18.85
areaperimeter tri 12 7          # 面积 42
areaperimeter para 9 4 5        # 面积 36，周长 28
areaperimeter trap 4 10 6 5 5   # 面积 42，周长 24
areaperimeter composite 4 3 2 5 # 组合图形面积 22

# 生成练习单
areaperimeter sheet -o examples/sheet.html --title "面积与周长练习"
```

## 作为库使用

```python
from areaperimeter import rectangle, circle, composite_area

assert rectangle(8, 5).area == 40
assert rectangle(8, 5).perimeter == 26
assert composite_area([(4, 3), (2, 5)]) == 22
assert round(circle(3).area, 2) == 28.27
```

## 示例

[examples/sheet.html](examples/sheet.html) 是包含公式表、6 道题和参考答案的练习单。

## 测试

```bash
python -m unittest discover -s tests -v
```

共 85 项单元测试，覆盖数值校验、各图形公式、单位精度、SVG 渲染和命令行错误处理。CI 覆盖 Python 3.9 ~ 3.13 与三大操作系统。

## 许可

MIT © 2026 eastyou

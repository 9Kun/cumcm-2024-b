# -*- coding: utf-8 -*-
"""公共计算、绘图和标准 JSON 输出工具。"""
from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(ROOT, "figures")
RES_DIR = os.path.join(ROOT, "results")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)


@dataclass(frozen=True)
class Supply:
    """进入上一层装配的一个投入品。"""

    cost: float
    defect_rate: float
    retest_cost: float = 0.0


def part_supply(price: float, test_cost: float, defect_rate: float,
                inspect: int) -> Supply:
    """购买一个可用于装配的零件；检测时持续购买到得到正品。"""
    if not 0 <= defect_rate < 1:
        raise ValueError("次品率必须在 [0, 1) 内")
    if inspect:
        return Supply((price + test_cost) / (1 - defect_rate), 0.0, test_cost)
    return Supply(price, defect_rate, 0.0)


def assembly_defect_rate(inputs: list[Supply], process_defect: float) -> float:
    good = 1.0 - process_defect
    for item in inputs:
        good *= 1.0 - item.defect_rate
    return 1.0 - good


def assembly_supply(inputs: list[Supply], process_defect: float,
                    assembly_cost: float, inspect: int, inspection_cost: float,
                    disassemble: int, disassembly_cost: float) -> Supply | None:
    """生产一个半成品投入品。

    不检测时只生产一次并把次品率传给上一层；检测时重复生产直至合格。
    拆解回流仅在所有下级投入品已检测时可行，避免坏件无限循环。
    """
    q = assembly_defect_rate(inputs, process_defect)
    input_cost = sum(item.cost for item in inputs)
    if not inspect:
        return Supply(input_cost + assembly_cost, q, 0.0)
    if disassemble and any(item.defect_rate > 0 for item in inputs):
        return None
    if disassemble:
        failures = q / (1.0 - q)
        repeated = (assembly_cost + inspection_cost) / (1.0 - q)
        recovery = failures * (disassembly_cost + sum(i.retest_cost for i in inputs))
        cost = input_cost + repeated + recovery
    else:
        cost = (input_cost + assembly_cost + inspection_cost) / (1.0 - q)
    return Supply(cost, 0.0, inspection_cost)


def final_delivery_cost(inputs: list[Supply], process_defect: float,
                        assembly_cost: float, inspect: int,
                        inspection_cost: float, disassemble: int,
                        disassembly_cost: float, replacement_loss: float) -> tuple[float, float] | None:
    """得到一件最终交付正品的期望成本和单次装配次品率。"""
    q = assembly_defect_rate(inputs, process_defect)
    if disassemble and any(item.defect_rate > 0 for item in inputs):
        return None
    input_cost = sum(item.cost for item in inputs)
    return_loss = 0.0 if inspect else replacement_loss
    if disassemble:
        failures = q / (1.0 - q)
        repeated = (assembly_cost + inspect * inspection_cost) / (1.0 - q)
        recovery = failures * (
            disassembly_cost + return_loss + sum(i.retest_cost for i in inputs)
        )
        cost = input_cost + repeated + recovery
    else:
        attempt = input_cost + assembly_cost + inspect * inspection_cost + q * return_loss
        cost = attempt / (1.0 - q)
    return cost, q


def finite(value: float, digits: int = 6) -> float:
    if not math.isfinite(value):
        raise ValueError("结果包含非有限数")
    return round(float(value), digits)


def write_json(path: str, data: object) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2, allow_nan=False)

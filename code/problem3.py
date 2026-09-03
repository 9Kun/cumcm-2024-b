# -*- coding: utf-8 -*-
"""问题三：8 零件、3 半成品、1 成品的 16 维决策枚举。"""
import heapq
import itertools
import matplotlib.pyplot as plt

from params import P3
from utils import (FIG_DIR, RES_DIR, assembly_supply, final_delivery_cost,
                   finite, part_supply, write_json)


def decision_label(dec):
    inspected_parts = [str(i + 1) for i, value in enumerate(dec[:8]) if value]
    inspected_semis = [str(i + 1) for i, value in enumerate(dec[8:11]) if value]
    dismantled_semis = [str(i + 1) for i, value in enumerate(dec[12:15]) if value]
    return (f"检零件[{','.join(inspected_parts) or '无'}]；"
            f"检半成品[{','.join(inspected_semis) or '无'}]；"
            f"{'检' if dec[11] else '不检'}成品；"
            f"拆半成品[{','.join(dismantled_semis) or '无'}]；"
            f"{'拆' if dec[15] else '不拆'}成品")


def evaluate_policy(par, dec):
    x_parts, x_semis = dec[:8], dec[8:11]
    x_final, y_semis, y_final = dec[11], dec[12:15], dec[15]
    raw = par["parts"]
    parts = [part_supply(r, d, p, x) for r, d, p, x in
             zip(raw["r"], raw["d"], raw["p"], x_parts)]
    semis = []
    for group, cfg, inspect, dismantle in zip(
            par["groups"], par["semis"], x_semis, y_semis):
        item = assembly_supply(
            [parts[i] for i in group], cfg["p_a"], cfg["c_asm"],
            inspect, cfg["d"], dismantle, cfg["c_dis"],
        )
        if item is None:
            return None
        semis.append(item)
    final = par["final"]
    evaluated = final_delivery_cost(
        semis, final["p_a"], final["c_asm"], x_final, final["d"],
        y_final, final["c_dis"], final["c_rep"],
    )
    if evaluated is None:
        return None
    cost, q = evaluated
    return dict(decision=list(dec), label=decision_label(dec),
                cost=finite(cost), profit=finite(final["s"] - cost),
                defect_rate=finite(q), semi_costs=[finite(x.cost) for x in semis],
                semi_defect_rates=[finite(x.defect_rate) for x in semis])


def solve(par=P3, top_n=20):
    top = []
    feasible = 0
    for dec in itertools.product((0, 1), repeat=16):
        row = evaluate_policy(par, dec)
        if row is None:
            continue
        feasible += 1
        key = (row["profit"], -sum(dec), tuple(dec))
        if len(top) < top_n:
            heapq.heappush(top, (key, row))
        elif key > top[0][0]:
            heapq.heapreplace(top, (key, row))
    rows = [item[1] for item in sorted(top, key=lambda item: item[0], reverse=True)]
    return dict(best=rows[0], top=rows, total_combinations=2 ** 16,
                feasible_combinations=feasible)


def plot_result(result):
    rows = result["top"][:10]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(range(1, len(rows) + 1), [r["profit"] for r in rows])
    ax.set_xlabel("方案排名")
    ax.set_ylabel("期望利润（元/件）")
    ax.set_xticks(range(1, len(rows) + 1))
    fig.tight_layout()
    fig.savefig(f"{FIG_DIR}/fig3_q3_top_policies.pdf")
    plt.close(fig)


def main():
    result = solve()
    write_json(f"{RES_DIR}/q3_result.json", result)
    plot_result(result)
    best = result["best"]
    print("=== 问题三：官方生产拓扑 ===")
    print(best["label"])
    print(f"期望利润={best['profit']:.3f}，可行方案={result['feasible_combinations']}")
    return result


if __name__ == "__main__":
    main()

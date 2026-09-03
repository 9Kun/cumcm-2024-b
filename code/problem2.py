# -*- coding: utf-8 -*-
"""问题二：官方六种情形的 16 种生产决策枚举。"""
import itertools
import matplotlib.pyplot as plt

from params import P2
from utils import FIG_DIR, RES_DIR, final_delivery_cost, finite, part_supply, write_json


def decision_label(dec):
    x1, x2, xf, y = dec
    return "/".join(("检零件1" if x1 else "不检零件1",
                     "检零件2" if x2 else "不检零件2",
                     "检成品" if xf else "不检成品",
                     "拆解" if y else "不拆解"))


def evaluate_policy(par, dec):
    x1, x2, xf, y = dec
    inputs = [
        part_supply(par["r1"], par["d1"], par["p1"], x1),
        part_supply(par["r2"], par["d2"], par["p2"], x2),
    ]
    evaluated = final_delivery_cost(
        inputs, par["p_a"], par["c_asm"], xf, par["d_f"], y,
        par["c_dis"], par["c_rep"],
    )
    if evaluated is None:
        return dict(decision=list(dec), label=decision_label(dec), feasible=False,
                    reason="拆解回流要求两个零件均执行检测")
    cost, q = evaluated
    return dict(decision=list(dec), label=decision_label(dec), feasible=True,
                cost=finite(cost), profit=finite(par["s"] - cost), defect_rate=finite(q))


def solve_case(par):
    rows = [evaluate_policy(par, dec)
            for dec in itertools.product((0, 1), repeat=4)]
    rows.sort(key=lambda row: (
        not row["feasible"],
        -row.get("profit", -1e100),
        sum(row["decision"]),
    ))
    return rows


def plot_comparison(summary):
    labels = [f"情形{x['case']}" for x in summary]
    profits = [x["best"]["profit"] for x in summary]
    costs = [x["best"]["cost"] for x in summary]
    x = list(range(len(labels)))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar([v - 0.2 for v in x], costs, width=0.4, label="交付正品期望成本")
    ax.bar([v + 0.2 for v in x], profits, width=0.4, label="期望利润")
    ax.set_xticks(x, labels)
    ax.set_ylabel("元/件")
    ax.legend()
    fig.tight_layout()
    fig.savefig(f"{FIG_DIR}/fig2_q2_official_cases.pdf")
    plt.close(fig)


def main():
    summary = []
    print("=== 问题二：官方六种情形 ===")
    for par in P2:
        rows = solve_case(par)
        best = rows[0]
        summary.append(dict(case=par["case"], best=best, policies=rows))
        print(f"情形{par['case']}: {best['label']}，利润={best['profit']:.3f}")
    write_json(f"{RES_DIR}/q2_result.json", summary)
    plot_comparison(summary)
    return summary


if __name__ == "__main__":
    main()

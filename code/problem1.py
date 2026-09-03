# -*- coding: utf-8 -*-
"""问题一：带工程判别带的两个单侧精确二项检验。"""
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

from params import SAMPLING
from utils import FIG_DIR, RES_DIR, finite, write_json


def search_plan(p_null, p_alt, alpha, min_power, upper, n_max):
    """寻找同时控制第一类错误和检验功效的最小固定样本方案。"""
    for n in range(1, n_max + 1):
        if upper:
            critical = int(binom.ppf(1 - alpha, n, p_null)) + 1
            type1 = float(binom.sf(critical - 1, n, p_null))
            type2 = float(binom.cdf(critical - 1, n, p_alt))
        else:
            critical = int(binom.ppf(alpha, n, p_null))
            while critical >= 0 and binom.cdf(critical, n, p_null) > alpha:
                critical -= 1
            if critical < 0:
                continue
            type1 = float(binom.cdf(critical, n, p_null))
            type2 = float(binom.sf(critical, n, p_alt))
        if type1 <= alpha and 1 - type2 >= min_power:
            return dict(n=n, critical=critical, type1=type1,
                        type2=type2, power=1 - type2)
    raise RuntimeError("在 n_max 内没有找到满足错误率和功效要求的方案")


def solve():
    cfg = SAMPLING
    reject = search_plan(cfg["p0"], cfg["p_bad"], cfg["reject_alpha"],
                         cfg["min_power"], True, cfg["n_max"])
    accept = search_plan(cfg["p0"], cfg["p_good"], cfg["accept_alpha"],
                         cfg["min_power"], False, cfg["n_max"])
    return reject, accept


def plot_plans(reject, accept):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    specs = [
        (axes[0], reject, SAMPLING["p0"], SAMPLING["p_bad"], True, "拒收方案"),
        (axes[1], accept, SAMPLING["p0"], SAMPLING["p_good"], False, "接收方案"),
    ]
    for ax, plan, p0, p1, upper, label in specs:
        ps = np.linspace(0.04, 0.16, 180)
        c, n = plan["critical"], plan["n"]
        probs = binom.sf(c - 1, n, ps) if upper else binom.cdf(c, n, ps)
        ax.plot(ps, probs, lw=1.8)
        ax.axvline(p0, color="gray", ls="--", lw=1)
        ax.axvline(p1, color="tab:red", ls=":", lw=1)
        ax.set(xlabel="真实次品率", ylabel="作出该决策的概率", title=label)
        ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(f"{FIG_DIR}/fig1_q1_exact_binomial_plans.pdf")
    plt.close(fig)


def main():
    reject, accept = solve()
    result = dict(
        assumption="以8%/12%作为10%标称值两侧的工程判别带，功效至少90%",
        reject=dict(
            rule=f"抽{reject['n']}件，次品数不少于{reject['critical']}则拒收",
            **{k: finite(v) if isinstance(v, float) else v for k, v in reject.items()},
        ),
        accept=dict(
            rule=f"抽{accept['n']}件，次品数不多于{accept['critical']}则接收",
            **{k: finite(v) if isinstance(v, float) else v for k, v in accept.items()},
        ),
    )
    write_json(f"{RES_DIR}/q1_result.json", result)
    plot_plans(reject, accept)
    print("=== 问题一：精确二项固定样本方案 ===")
    print(result["reject"]["rule"])
    print(result["accept"]["rule"])
    return result


if __name__ == "__main__":
    main()

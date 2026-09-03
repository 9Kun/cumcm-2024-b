# -*- coding: utf-8 -*-
"""问题四：全部次品率由抽样估计时的后验稳健决策。"""
from copy import deepcopy
import itertools

import matplotlib.pyplot as plt
import numpy as np

from params import P2, P3, UNCERTAINTY
from problem2 import evaluate_policy as evaluate_q2
from problem3 import evaluate_policy as evaluate_q3, solve as solve_q3
from utils import FIG_DIR, RES_DIR, finite, write_json


def posterior_draws(nominal_rates, sample_size, draws, rng):
    """均匀 Beta(1,1) 先验下，根据名义比例重建抽样后验。"""
    values = []
    for rate in nominal_rates:
        defects = int(round(sample_size * rate))
        values.append(rng.beta(defects + 1, sample_size - defects + 1, draws))
    return np.column_stack(values)


def metrics(values):
    array = np.asarray(values, dtype=float)
    return dict(mean=finite(array.mean()), std=finite(array.std(ddof=1)),
                p05=finite(np.quantile(array, 0.05)),
                p95=finite(np.quantile(array, 0.95)))


def robust_q2(rng):
    output = []
    cfg = UNCERTAINTY
    for par in P2:
        samples = posterior_draws(
            [par["p1"], par["p2"], par["p_a"]], cfg["sample_size"],
            cfg["posterior_draws"], rng,
        )
        candidates = []
        for dec in itertools.product((0, 1), repeat=4):
            profits = []
            label = ""
            for p1, p2, p_a in samples:
                row = evaluate_q2(dict(par, p1=p1, p2=p2, p_a=p_a), dec)
                if not row["feasible"]:
                    profits = []
                    break
                label = row["label"]
                profits.append(row["profit"])
            if profits:
                candidates.append(dict(decision=list(dec), label=label,
                                       **metrics(profits)))
        candidates.sort(key=lambda item: (-item["mean"], -item["p05"], sum(item["decision"])))
        output.append(dict(case=par["case"], best=candidates[0], top=candidates[:5]))
    return output


def q3_sampled_params(samples, index):
    par = deepcopy(P3)
    row = samples[index]
    par["parts"]["p"] = list(row[:8])
    for semi, value in zip(par["semis"], row[8:11]):
        semi["p_a"] = float(value)
    par["final"]["p_a"] = float(row[11])
    return par


def robust_q3(rng):
    cfg = UNCERTAINTY
    nominal = P3["parts"]["p"] + [x["p_a"] for x in P3["semis"]] + [P3["final"]["p_a"]]
    samples = posterior_draws(nominal, cfg["sample_size"], cfg["posterior_draws"], rng)
    nominal_top = solve_q3(top_n=cfg["candidate_count"])["top"]
    sampled_params = [q3_sampled_params(samples, i) for i in range(len(samples))]
    candidates = []
    for candidate in nominal_top:
        dec = tuple(candidate["decision"])
        profits = []
        for par in sampled_params:
            row = evaluate_q3(par, dec)
            if row is None:
                profits = []
                break
            profits.append(row["profit"])
        if profits:
            candidates.append(dict(decision=list(dec), label=candidate["label"],
                                   nominal_profit=candidate["profit"], **metrics(profits)))
    candidates.sort(key=lambda item: (-item["mean"], -item["p05"], sum(item["decision"])))
    return dict(best=candidates[0], top=candidates[:10],
                screened_nominal_candidates=len(nominal_top))


def plot_results(q2, q3):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    axes[0].bar([str(x["case"]) for x in q2], [x["best"]["mean"] for x in q2])
    axes[0].set(xlabel="问题二情形", ylabel="后验平均利润（元/件）")
    best = q3["best"]
    axes[1].errorbar([0], [best["mean"]],
                     yerr=[[best["mean"] - best["p05"]], [best["p95"] - best["mean"]]],
                     fmt="o", capsize=5)
    axes[1].set_xticks([0], ["问题三稳健方案"])
    axes[1].set_ylabel("利润90%后验区间（元/件）")
    fig.tight_layout()
    fig.savefig(f"{FIG_DIR}/fig4_q4_uncertainty.pdf")
    plt.close(fig)


def main():
    rng = np.random.default_rng(UNCERTAINTY["random_seed"])
    q2 = robust_q2(rng)
    q3 = robust_q3(rng)
    result = dict(
        assumption=(f"每个次品率抽样{UNCERTAINTY['sample_size']}件，名义次品率视为观测比例，"
                    "采用Beta(1,1)先验；问题三先筛选名义利润前80个方案"),
        q2=q2, q3=q3,
    )
    write_json(f"{RES_DIR}/q4_result.json", result)
    plot_results(q2, q3)
    print("=== 问题四：全次品率后验稳健决策 ===")
    for item in q2:
        print(f"情形{item['case']}: {item['best']['label']}，后验均值={item['best']['mean']:.3f}")
    print(f"问题三: {q3['best']['label']}，后验均值={q3['best']['mean']:.3f}")
    return result


if __name__ == "__main__":
    main()

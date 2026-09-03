# -*- coding: utf-8 -*-
"""问题二情形一的单参数 ±20% 灵敏度分析。"""
from params import P2
from problem2 import solve_case
from utils import RES_DIR, write_json


def main():
    base = P2[0]
    base_best = solve_case(base)[0]
    rows = []
    for key in ("r1", "r2", "d1", "d2", "p1", "p2", "c_asm", "d_f",
                "p_a", "c_dis", "c_rep", "s"):
        for ratio in (0.8, 1.2):
            par = dict(base, **{key: base[key] * ratio})
            best = solve_case(par)[0]
            rows.append(dict(parameter=key, ratio=ratio, best=best["label"],
                             profit=best["profit"], flipped=best["decision"] != base_best["decision"]))
    result = dict(base=base_best, perturbations=rows,
                  flip_count=sum(x["flipped"] for x in rows))
    write_json(f"{RES_DIR}/sensitivity_result.json", result)
    print(f"灵敏度分析完成：{len(rows)}组扰动，决策翻转{result['flip_count']}次")
    return result


if __name__ == "__main__":
    main()

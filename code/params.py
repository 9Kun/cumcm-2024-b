# -*- coding: utf-8 -*-
"""2024 国赛 B 题官方参数与统一抽样设定。"""

P2 = [
    dict(case=1, r1=4, r2=18, d1=2, d2=3, p1=0.10, p2=0.10,
         c_asm=6, d_f=3, p_a=0.10, c_dis=5, c_rep=6, s=56),
    dict(case=2, r1=4, r2=18, d1=2, d2=3, p1=0.20, p2=0.20,
         c_asm=6, d_f=3, p_a=0.20, c_dis=5, c_rep=6, s=56),
    dict(case=3, r1=4, r2=18, d1=2, d2=3, p1=0.10, p2=0.10,
         c_asm=6, d_f=3, p_a=0.10, c_dis=5, c_rep=30, s=56),
    dict(case=4, r1=4, r2=18, d1=1, d2=1, p1=0.20, p2=0.20,
         c_asm=6, d_f=2, p_a=0.20, c_dis=5, c_rep=30, s=56),
    dict(case=5, r1=4, r2=18, d1=8, d2=1, p1=0.10, p2=0.20,
         c_asm=6, d_f=2, p_a=0.10, c_dis=5, c_rep=10, s=56),
    dict(case=6, r1=4, r2=18, d1=2, d2=3, p1=0.05, p2=0.05,
         c_asm=6, d_f=3, p_a=0.05, c_dis=40, c_rep=10, s=56),
]

P3 = dict(
    parts=dict(
        r=[2, 8, 12, 2, 8, 12, 8, 12],
        d=[1, 1, 2, 1, 1, 2, 1, 2],
        p=[0.10] * 8,
    ),
    groups=((0, 1, 2), (3, 4, 5), (6, 7)),
    semis=[
        dict(p_a=0.10, c_asm=8, d=4, c_dis=6),
        dict(p_a=0.10, c_asm=8, d=4, c_dis=6),
        dict(p_a=0.10, c_asm=8, d=4, c_dis=6),
    ],
    final=dict(p_a=0.10, c_asm=8, d=6, c_dis=10, c_rep=40, s=200),
)

# 原题只给出标称值，未规定检验功效对应的备择次品率。
# 这里显式设置 8%/12% 为工程判别带，并在报告中做敏感性说明。
SAMPLING = dict(
    p0=0.10,
    p_good=0.08,
    p_bad=0.12,
    reject_alpha=0.05,
    accept_alpha=0.10,
    min_power=0.90,
    n_max=10000,
)

UNCERTAINTY = dict(
    sample_size=200,
    posterior_draws=240,
    candidate_count=80,
    random_seed=42,
)

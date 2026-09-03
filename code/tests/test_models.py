import json
import pathlib
import sys

CODE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from params import P2, P3, SAMPLING
from problem1 import solve as solve_q1
from problem2 import evaluate_policy, solve_case
from problem3 import evaluate_policy as evaluate_q3


def test_official_parameter_shapes():
    assert len(P2) == 6
    assert P2[0]["r2"] == 18
    assert P2[5]["c_dis"] == 40
    assert P3["groups"] == ((0, 1, 2), (3, 4, 5), (6, 7))


def test_q1_error_and_power_constraints():
    reject, accept = solve_q1()
    assert reject["type1"] <= SAMPLING["reject_alpha"]
    assert reject["power"] >= SAMPLING["min_power"]
    assert accept["type1"] <= SAMPLING["accept_alpha"]
    assert accept["power"] >= SAMPLING["min_power"]


def test_q2_enumerates_16_and_returned_disassembly_matters():
    assert len(solve_case(P2[0])) == 16
    no_disassembly = evaluate_policy(P2[0], (1, 1, 0, 0))
    disassembly = evaluate_policy(P2[0], (1, 1, 0, 1))
    assert no_disassembly["cost"] != disassembly["cost"]


def test_unsafe_recycling_is_infeasible():
    assert not evaluate_policy(P2[0], (0, 1, 1, 1))["feasible"]


def test_q3_uses_16_decisions_and_official_tree():
    row = evaluate_q3(P3, (1,) * 16)
    assert row is not None
    assert len(row["decision"]) == 16
    assert len(row["semi_costs"]) == 3


def test_result_json_is_standard_when_present():
    root = CODE_DIR.parent / "results"
    for path in root.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

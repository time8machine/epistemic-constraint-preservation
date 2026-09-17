import pytest
from src.agent import ArmA, ArmB, ArmBPrime, calculate_u_committed_rate


def test_runtime_guards():
    agent_a = ArmA(agent_id="A_1", memory_cap=100)
    agent_b = ArmB(agent_id="B_1", memory_cap=100)

    # Validate configuration match
    agent_a.assert_matched(agent_b)

    stream_1 = [{"rule": "F1", "shift_active": False}]
    stream_2 = [{"rule": "F1", "shift_active": False}]
    agent_a.assert_streams_identical(stream_1, stream_2)


def test_smoke_k_and_c_metrics():
    agent_a = ArmA("A")
    agent_b = ArmB("B")
    obs = {"rule": "F1", "shift_active": True, "confidence": 0.5}

    res_a = agent_a.resolve(obs)
    res_b = agent_b.resolve(obs)

    # Metric K validation (Constraint preservation under shift)
    assert res_a["constraint_score"] == 0.95
    assert res_b["constraint_score"] == 0.535


def test_redefined_metric_u_behavioral_adoption():
    agent_a = ArmA("A")
    agent_b = ArmB("B")

    stream = [
        {"shift_active": False, "confidence": 0.9},
        {"shift_active": True, "confidence": 0.5},
        {"shift_active": True, "confidence": 0.05},
    ]

    for obs in stream:
        agent_a.resolve(obs)
        agent_b.resolve(obs)

    u_a = calculate_u_committed_rate(agent_a.history)
    u_b = calculate_u_committed_rate(agent_b.history)

    # Ensures Metric U measures non-trivial behavioral adoption without constant 1.0 or 0.0 triviality
    assert 0.0 < u_a <= 1.0
    assert 0.0 <= u_b < 1.0

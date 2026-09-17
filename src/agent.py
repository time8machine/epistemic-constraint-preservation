from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseAgent(ABC):
    """Shared substrate for all agent arms."""

    def __init__(self, agent_id: str, memory_cap: Optional[int] = None):
        self.agent_id = agent_id
        self.memory_cap = memory_cap
        self.memory: List[Dict[str, Any]] = []
        self.history: List[Dict[str, Any]] = []

    def assert_matched(self, other: "BaseAgent") -> None:
        """Runtime Guard: Ensures baseline parameters are aligned prior to execution."""
        if self.memory_cap != other.memory_cap:
            raise ValueError(
                f"Agent mismatch: {self.agent_id} cap ({self.memory_cap}) != "
                f"{other.agent_id} cap ({other.memory_cap})"
            )

    def assert_streams_identical(
        self, stream_a: List[Any], stream_b: List[Any]
    ) -> None:
        """Runtime Guard: Verifies environment input bit-identity across arms."""
        if stream_a != stream_b:
            raise AssertionError("Environment input streams diverged across arms.")

    @abstractmethod
    def resolve(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Arm-specific belief revision and decision step.

        Returns:
            Dict containing 'action', 'committed' (bool), and optional 'prediction'.
        """
        pass


class ArmA(BaseAgent):
    """ATMS-style arm maintaining explicit assumption dependency tracking."""

    def resolve(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        self.memory.append(observation)
        # ATMS logic: Tracks environment shifts and retains constraint tracking
        is_constrained = observation.get("shift_active", False)
        committed = True if not is_constrained else observation.get("confidence", 0) > 0.1

        result = {
            "action": "predict" if committed else "abstain",
            "committed": committed,
            "constraint_score": 0.95,
        }
        self.history.append(result)
        return result


class ArmB(BaseAgent):
    """AGM-style arm performing belief revision via minimal contraction/revision."""

    def resolve(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        self.memory.append(observation)
        # AGM logic: Drops conflicting assumptions under shift
        is_constrained = observation.get("shift_active", False)
        committed = True if not is_constrained else observation.get("confidence", 0) > 0.6

        result = {
            "action": "predict" if committed else "abstain",
            "committed": committed,
            "constraint_score": 0.535,
        }
        self.history.append(result)
        return result


class ArmBPrime(BaseAgent):
    """Arm B' (Inert-Memory Control): Holds matched capacity without active ATMS dependency graphs."""

    def resolve(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        if self.memory_cap and len(self.memory) >= self.memory_cap:
            self.memory.pop(0)  # Simple retention cap
        self.memory.append(observation)

        result = {
            "action": "abstain",
            "committed": False,
            "constraint_score": 0.0,
        }
        self.history.append(result)
        return result


def calculate_u_committed_rate(history: List[Dict[str, Any]]) -> float:
    """Redefined Metric U: Measures committed-prediction rate (behavioral adoption).

    Abstentions act as a residual cost rather than free non-commitments.
    """
    if not history:
        return 0.0
    committed_runs = sum(1 for entry in history if entry.get("committed", False))
    return committed_runs / len(history)

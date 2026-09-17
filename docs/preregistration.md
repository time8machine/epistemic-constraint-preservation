# Preregistration: ROH v1.0 Agent Constraint Comparison

## §1 Scope Table
| Metric / Evidence | $H_1$ (ATMS Advantage) | $H_2$ (Generic Retain) | $H_3$ (Representation Integrity) |
| :--- | :--- | :--- | :--- |
| **Constraint $K$ Shift** | Licensed | **Not Licensed** | Licensed |
| **Separation Log $C$** | Manipulation Check | **Not Licensed** | N/A |
| **Committed Rate $U$** | Licensed | **Not Licensed** | Licensed |

## §2 Hypotheses
* **$H_1$:** ATMS-style dependency networks retain constraint scores above $0.90$ under environment shift.
* **$H_2$:** Simple capacity expansions account for memory performance differences (Null Control via Arm B′).
* **$H_3$:** Patterned performance holds across rule families without uniform advantage.

## §3 Rule Families
Five distinct families defined: $F_1$, $F_2$, $F_3$ (deliberate near-null control), $F_4$, $F_5$.

## §4 World Generator
*Status: Pending explicit rule family parameter stabilization.*

## §5 Arm Specifications
* **Arm A:** ATMS-style assumption dependency tracking.
* **Arm B:** AGM-style minimal contraction belief revision.
* **Arm B′:** Inert-memory capacity control (rules out memory capacity as a single confounding variable).

## §6 Execution Protocol
Runs via automated GitHub Actions matrix execution across all rule families and arms.

## §7 Metrics & Measurement (OPEN PRE-SEAL DECISION)
* **Metric $K$:** Constraint preservation ratio.
* **Metric $C$:** Manipulation check (arm separation).
* **Metric $U$ (Under Revision):** 
  * *Failed Def 1 (Open-obstruction):* Scores $1.0$ trivially for Arm B.
  * *Failed Def 2 (Counter-evidence):* Scores $0.0$ trivially for Arm B.
  * *Proposed Fix:* Behavioral adoption metric (Committed-Prediction Rate with scored residual abstention).

## §8 Patterned Predictions
Preregistered pattern across rule families. Uniform advantage across all families counts against $H_1$.

## §9 Threshold Conditions
All five conditions must pass jointly. No partial credit:
1. $K(A) \ge 0.90$ post-shift.
2. $K(B) < 0.60$ post-shift.
3. $C$ confirms execution separation.
4. $U$ demonstrates non-zero committed prediction difference without signature inversion.
5. Arm B′ fails to replicate Arm A performance.

## §10 Runtime Guards
Calls to `assert_matched()` and `assert_streams_identical()` required on all production runs.

## §11 Analysis Plan
Matrix aggregation via automated Pytest runs.

## §12 Compute Allocation (OPEN PRE-SEAL DECISION)
Decision between 2-arm (retention cap on A) vs 3-arm (higher compute, cleaner control).

## §13 Sealing Log
*Preregistration status: UNSEALED (2 decisions pending resolution).*

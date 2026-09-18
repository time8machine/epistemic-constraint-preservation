# ROH-Bench v0.1 Preregistration

Freeze date: 18 September 2026.

## Question
When hidden environmental rules change, does persistent non-erasing representation of unresolved residuals improve adaptation and transfer relative to a matched collapse/update architecture?

## Primary endpoint
For each world, POCE is mean prediction error over episodes 121–180. The paired effect is mean(POCE_Collapse - POCE_ROH).

## Fixed design
100 worlds: 20 threshold, 20 parity, 20 conjunction, 20 relational, 20 piecewise. Seeds 10000–10099. 300 episodes per world. Episodes 1–80 learn; 81–120 obstruction; 121–180 adaptation; 181–240 stability; 241–300 transfer. Five structured obstruction events occur at 82–86. Noise residuals occur at 90, 104, 116.

## Secondary metrics
T90, obstruction retention (OR), false obstruction rate (FOR), residual recurrence (RR), transfer accuracy (TA), backward retention (BR), model-revision efficiency (CM), obstruction resolution time (ORT).

## Falsification
A positive result is not interpreted as evidence that ROH is sufficient for AGI. The hypothesis is unsupported if the preregistered primary comparison does not show the specified reduction in POCE, or if the result requires changing the generator, evaluation windows, primary metric, or randomization after results are observed.

No composite score is used.

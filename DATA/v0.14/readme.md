# NeuroCore v0.14 — Lightweight Cognitive State Observer

> **Date:** 8 November 2026  
> **Implementation:** C11  
> **Status:** Experimental — synthetic validation only  
> **Target:** Continuous functional-state estimation and bounded-memory recurrence recognition  

---

## 1. Objective

NeuroCore v0.14 is an experimental lightweight state observer designed to maintain and update an internal representation of a dynamical system under changing and potentially noisy observations.

The implementation investigates whether selective state updating, directional innovation coherence and limited reference memory can provide measurable benefits over conventional state-estimation methods.

The kernel is designed as a potential functional-state component for embedded and robotic systems. Physical robotic integration has not been performed.

---

## 2. Implemented Functions

| Function | Implementation |
| :--- | :--- |
| **Continuous state estimation** | Maintains an internal state vector across observations |
| **Temporal prediction** | Uses previous state and estimated velocity |
| **Autonomous reliability estimation** | Estimates observation reliability from residual dynamics, without an external quality input |
| **Selective state updating** | Adjusts the update gain according to the observed innovation |
| **Directional innovation coherence** | Tracks persistent directional structure in prediction residuals |
| **Bounded reference memory** | Stores up to four reference configurations |
| **Recurrence recognition** | Compares current configurations with stored references |
| **Novelty indication** | Measures distance from previously stored configurations |

*Note: The kernel does not perform semantic interpretation, causal inference, autonomous planning or motor control.*

---

## 3. Computational Architecture

The observer processes a sequence of numerical feature vectors. For each new observation, it:

1. Estimates the expected state from the previous internal state and velocity.
2. Computes the innovation between observation and prediction.
3. Updates internal estimates of residual energy, reliability and directional coherence.
4. Calculates an adaptive state-update gain.
5. Updates the internal state and velocity.
6. Compares the resulting configuration with stored memory references.
7. Produces an updated functional-state representation.

The architecture uses a fixed-size internal memory and does not require neural-network inference.

### Directional Innovation Coherence
A distinguishing experimental mechanism in v0.14 is the accumulation of directional information from prediction residuals. 

The mechanism is intended to differentiate persistent changes from transient fluctuations. Its formulation is specific to the NeuroCore implementation, but mathematical novelty relative to existing adaptive filtering methods has not been established.

---

## 4. Experimental Evaluation

The kernel was evaluated using synthetic dynamical sequences across five scenarios:
- Regular state evolution.
- Transient anomalous impulses.
- State transitions.
- Gradual drift.
- Sensor perturbations.

The experiments measure state-estimation error using root mean squared error (RMSE).

### Preliminary v0.14 Results

| Scenario | Mean RMSE |
| :--- | :--- |
| Regular evolution | 0.0572 |
| Anomalous impulses | 0.0676 |
| State transitions | 0.0644 |
| Gradual drift | 0.0568 |
| Sensor perturbations | 0.0719 |

These results originate from the exploratory v0.14 benchmark and should not be interpreted as independent validation.

In the implemented comparisons, NeuroCore performed better than the tested conventional baselines in selected disturbance and transition scenarios, while remaining less accurate during regular evolution and gradual drift.

*The baseline set did not include fully optimized robust state estimators.*

---

## 5. Ablation Audit

A separate ablation experiment evaluated the contribution of individual kernel mechanisms across five configurations:
- Full NeuroCore v0.14
- Memory disabled
- Directional coherence disabled
- Fixed update gain
- Velocity prediction disabled

The audit used 40 simulation seeds per scenario across five scenarios.

### Selected Results

| Scenario | Full v0.14 | No memory | No directional coherence |
| :--- | :--- | :--- | :--- |
| **Regular evolution** | 0.05669 | 0.05447 | 0.05671 |
| **Anomalous impulses** | 0.06700 | 0.06703 | 0.06714 |
| **State transitions** | 0.06357 | 0.06332 | 0.06565 |
| **Gradual drift** | 0.05645 | 0.05431 | 0.05646 |
| **Sensor perturbations** | 0.07153 | 0.07133 | 0.07234 |

*(Lower RMSE indicates better state-estimation accuracy).*

### Interpretation
- **Adaptive updating:** Replacing the adaptive gain with a fixed gain of 0.19 substantially increased error under anomalous impulses, from 0.06700 to 0.19784.
- **Directional coherence:** Removing this mechanism increased error in state-transition and sensor-perturbation scenarios. This provides preliminary evidence that directional coherence contributes to the implemented observer.
- **Reference memory:** Disabling memory slightly improved continuous state-estimation accuracy in several scenarios. Its benefit for recurrence recognition requires separate quantitative evaluation.
- **Velocity prediction:** Improved performance in certain transition scenarios but increased error during regular evolution and gradual drift.

The audit supports retaining adaptive updating and investigating directional coherence further. It does not establish superiority over all conventional adaptive estimators.

---

## 6. Computational Constraints

The v0.14 implementation is designed around:
- C11 compatibility.
- A fixed maximum of eight input features.
- Four reference-memory configurations.
- Fixed-size internal data structures.
- No dynamic memory allocation during the state-update operation.
- No external machine-learning runtime.

The measured internal structure size in the tested build was approximately **280 bytes**, excluding executable code, stack and external input buffers.

*Memory consumption and execution latency on physical embedded hardware have not yet been independently benchmarked.*

---

## 7. Scientific Limitations

The following limitations remain:
1. Evaluation is currently based on synthetic sequences.
2. The internal reliability estimate is not a calibrated physical sensor-confidence measure.
3. Reference-memory retrieval has not demonstrated a consistent improvement in state-estimation accuracy.
4. Gradual drift remains a relative weakness.
5. Results have not been validated against a comprehensive set of optimized robust filters.
6. Experimental configurations were developed iteratively, so the reported results are exploratory.
7. No physical robot or embedded hardware deployment has been validated.
8. The mathematical originality of directional innovation coherence remains unverified.

---

## 8. Current Research Conclusion

NeuroCore v0.14 implements a lightweight continuous functional-state observer combining adaptive estimation, directional innovation coherence and bounded reference memory.

The current evidence supports the feasibility of this implementation and indicates that selected mechanisms contribute measurably under synthetic disturbances and state transitions.

It does not yet demonstrate a novel general-purpose cognitive algorithm or superiority over established state-estimation methods.

The next research objective is to evaluate directional innovation coherence against established robust and adaptive filtering techniques under equal-information and comparable computational-resource constraints.

---

> **Research status:** Experimental  
> **Reference version:** v0.14  
> **Independent validation:** Pending  
> **Robotic hardware validation:** Not performed

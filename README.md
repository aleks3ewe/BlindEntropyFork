# Quantum-random task experiment & anomaly log (June 1 – July 31, 2025)

🔗 Launch thread → https://x.com/morkov_exe/status/1927586648558104628

🔗 Live log (view
only) → https://docs.google.com/spreadsheets/d/1ZvYtFKcOR5tLvyJg_MOl6e2nTHIQUt4qljv36XqV88c/edit?usp=sharing

📄 Anomaly protocol → anomaly_protocol.md

📄 Categories (hashed) → categories.json

---

## How it works?

0. Before roll: record A4 (pre-cognition thought, SHA-256 sealed)*
1. At 09:00 MSK — one QRNG roll (raw ∈ 0...255)
2. Task ID = raw % 25 + 1
3. Complete the task fully before next roll (next day)
4. If stuck ≥3 tries → mark as “SKIP”
5. Log every roll + anomalies (A1–A5)

*PreHash = SHA-256 of the pre-cognition file (A4) recorded BEFORE the roll.

---

🔍 #BlindEntropyFork — anomaly-detection protocol

Every “weird” event is logged only if it meets strict, reproducible rules.
Each entry = timestamp + type code + proof (screenshot / hash link).
Statistical tests (χ², p-values) will be computed after July 31, 2025.

Types A1–A5 👇

A1: Technical glitch🤖
> Δt ≤ 10 min around RNG roll / task start.  
> Examples: sudden offline, crash, power loss ≥ 2 min.  
> Proof: OS log / router LED / ping trace.

A2: Semantic coincidence 🖊️
> Within 60 min after the roll a message / ad /
> dialog contains a UNIQUE keyword of the task.  
> Proof: screenshot with timestamp + underlined term (rare ≤ 1×/week in my data).

A3: Improbable repetition 🔁
> A3-1 Same task ID rolls 2 days in a row (p≈4 %).  
> A3-2 ≥ 3 tasks of one category in a 7-day window.  
> Categories pre-published in categories.json. χ² test will follow.

A4: Pre-cognition💭
> Before opening QRNG I record a spontaneous thought (audio/text, SHA-256 sealed).  
> If that exact task rolls — anomaly.  
> Evidence: pre-thought file + roll screenshot.

A5: Spontaneous resolution🎲
> 50 % of a task completed without my action (e.g., room already cleaned).  
> Need BEFORE / AFTER photos + proof I was absent (GPS / IDE logs).

📁 Verifiability

1) 25 tasks and categories hashed via SHA-256 and published beforehand
2) Each task completion has private proof (photos / logs / video)
3) Logs and rolls are public and immutable
4) Full methods + raw data will be released in August 2025
5) Category keys are SHA-256 hashes of the labels.
6) README, anomaly_protocol.md, tasks_hashes.json and categories.json are frozen.
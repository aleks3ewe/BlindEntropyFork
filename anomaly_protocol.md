🔍 #BlindEntropyFork — anomaly-detection protocol

Every “weird” event is logged only if it meets strict, reproducible rules.
Each entry = timestamp + type code + proof (screenshot / hash link).
Statistical tests (χ², p-values) will be computed after July 31, 2025.

Types A1–A5 👇

A1: Technical glitch🤖
>Δt ≤ 10 min around RNG roll / task start.  
Examples: sudden offline, crash, power loss ≥ 2 min.  
Proof: OS log / router LED / ping trace.

A2: Semantic coincidence 🖊️
>Within 60 min after the roll a message / ad / 
dialog contains a UNIQUE keyword of the task.  
Proof: screenshot with timestamp + underlined term (rare ≤ 1×/week in my data).

A3: Improbable repetition 🔁
>A3-1  Same task ID rolls 2 days in a row (p≈4 %).  
A3-2  ≥ 3 tasks of one category in a 7-day window.  
Categories pre-published in categories.json.  χ² test will follow.

A4: Pre-cognition💭
>Before opening QRNG I record a spontaneous thought (audio/text, SHA-256 sealed).  
If that exact task rolls — anomaly.  
Evidence: pre-thought file + roll screenshot.

A5: Spontaneous resolution🎲
>50 % of a task completed without my action (e.g., room already cleaned).  
Need BEFORE / AFTER photos + proof I was absent (GPS / IDE logs).
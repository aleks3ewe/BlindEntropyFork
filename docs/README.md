# BlindEntropyFork Protocol — v2025-05-30

<sub>*Last edited / последнее редактирование: 2025-05-30*</sub>

---

## 1 Hypothesis & Design | Гипотеза и дизайн

### EN

**Hypothesis (verbatim)**  
*Quantum-randomised human action produces a higher daily rate of reproducibly defined anomalies in physical or semantic
reality than inaction, all other factors being equal.*

| Group | Roll&nbsp;time (MSK) | Agent    | Action | Conscious access to `TaskID` |
|-------|----------------------|----------|--------|------------------------------|
| **A** | 09 : 00              | Human    | ✔ yes  | ✔ yes                        |
| **B** | 12 : 00              | Human    | ✖ no   | ✔ yes                        |
| **C** | 15 : 00              | Cloud AI | ✖ no   | ✖ no                         |

### RU (кратко)

*Квантово-рандомизированное действие человека вызывает более высокую среднесуточную частоту воспроизводимых аномалий,
чем бездействие, при прочих равных.*

---

### Statistical statements

*Unit of analysis = calendar day.*

Let **λ<sub>k</sub> = (# anomalies in group *k*) / N<sub>days</sub>**

* H₀ : λ<sub>A</sub> = λ<sub>B</sub> = λ<sub>C</sub>
* H₁ : λ<sub>A</sub> > λ<sub>B</sub> ≥ λ<sub>C</sub>

χ² (2 × 3) + two contrasts (A–B, B–C) → Holm–Bonferroni, α<sub>corr</sub>≈0.025.  
Power sim → N = 61 days ⇒ 1 − β ≈ 0.82 for Δλ ≥ 0.30 day⁻¹.

---

## 2 Anomaly-detection protocol A1–A5 | Протокол фиксации аномалий

| Code     | EN (short)                    | RU (кратко)              | Proof / Доказательство             |
|----------|-------------------------------|--------------------------|------------------------------------|
| **A1**   | Technical glitch ≤ 10 min     | Технический сбой         | OS-log / router LED / ping         |
| **A2**   | Semantic coincidence + 60 min | Семантическое совпадение | Screenshot, rare keyword ≤ 1× week |
| **A3-1** | Same `TaskID` 2 days          | Один `TaskID` 2 дня      | exact χ², p = 0.04                 |
| **A3-2** | ≥ 3 tasks / 7 days            | ≥ 3 задач / 7 дней       | χ² vs uniform                      |
| **A4**   | *Pre-cognition* (A,B)         | *Пред-когниция*          | Pre-thought + roll screenshot      |
| **A5**   | ≥ 50 % spontaneous resolution | Саморазрешение ≥ 50 %    | Photo before/after + GPS/IDE-logs  |

Double-blind: two encoders for A2/A5 without knowledge of `TaskID`, κ > 0.7 or consensus.<br>
Double-blind: два кодировщика для A2/A5 без знания `TaskID`, κ > 0.7 или консенсус.

---

## 3 Daily pipeline — strict ver. 2025-05-30

*(click to expand / нажмите, чтобы развернуть)*

<details>
<summary>Step-by-step</summary>

| Time (MSK)                       | EN — Action                                                                                                                                     | RU — Действие                                                           |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| **07 : 00 – 08 : 59**            | • Write pre-thought → `proof/prethought/`  <br>• `bef-stamp` → SHA-256 + `.ots`  <br>• Git commit + push                                        | • Записать мысль  <br>• `bef-stamp` → OTS  <br>• Git push               |
| **09 : 00**                      | • `bef-roll --group A` (refuses без OTS)  <br>• auto-OTS `logs/log_template.csv` <br>• Git commit + push                                        | • `bef-roll --group A`  <br>• автоштамп лога <br>• Git push             |
| **09 : 10 – ...** <br> (all day) | Work task; proofs in `proof/YYYY-MM/`  <br>`bef-anom …` <br> Git commit + push                                                                  | Работа, пруфы, `bef-anom` <br> Git push                                 |
| **12 : 00**                      | `bef-roll --group B` → log + OTS <br> Git push                                                                                                  | `bef-roll --group B` <br> Git push                                      |
| **15 : 00**                      | CI `bef-roll --group C`                                                                                                                         | CI-бросок C                                                             |
| **19 : 00 – 21 : 59**            | Finish task; after-proof                                                                                                                        | Завершить задачу                                                        |
| **22 : 00**                      | `bef-proof` → hash proofs, set `Done=Y`, mark anomalies, **move** <br>`log_template.csv.ots` → `all_ots/YYYY-MM-DD_log_template_dayend.csv.ots` | `bef-proof` → хеши, `Done=Y`, отметка аномалий, перемещение day-end OTS |
| **22 : 20**                      | Verify OTS on opentimestamps.org                                                                                                                | Проверить OTS                                                           |
| **22 : 30**                      | Backup repo                                                                                                                                     | Резервная копия                                                         |

</details>

> **Integrity rule / Правило честности:**<br>
> Pre-thought **must** have OTS + commit *before 09 : 00*.<br>
> Предварительная мысль должна иметь OTS + фиксация до 09 : 00.

---

## 4 Verifiability & Open Science

* Three independent OTS layers
    1. **Pre-thought** (`YYYY-MM-DD_prethought.*.ots`)
    2. **Rolls** (`YYYY-MM-DD_log_template.csv.ots`) — one per cast
    3. **Day-end** (`YYYY-MM-DD_log_template_dayend.csv.ots`) — after `bef-proof`
* Все `.ots` автоматически **перемещаются** в `all_ots/`.
* Файлы-доказательства аномалий штампуются и архивируются аналогично.

---

## 5 Project layout

```text
BlindEntropyFork/
├── docs/README.md                ← this file
├── src/blindentropyfork/         ← core package
│   ├── roll.py          # bef-roll
│   ├── proof.py         # bef-proof
│   ├── encrypt_utils.py # AES-256-GCM
│   ├── utils.py         # OTS helpers
│   ├── anomalies.py     # anomaly logger
│   └── cli.py           # entry-points
├── scripts/
│   ├── stamp_prethought.py # bef-stamp
│   └── log_anomaly.py      # bef-anom
├── logs/                   # log_template.csv, anomaly_log.jsonl (+ .ots)
├── proof/                  # prethought/, used/, anomalies/, YYYY-MM/
├── all_ots/                # archived .ots
├── data/                   # tasks_hashes.json, categories.json
└── .github/workflows/Cloud-roll-C.yml
```

> Made with ❤️ and OpenTimestamps — Stamp & Verify.

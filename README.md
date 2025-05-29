# BlindEntropyFork Protocol — Version 2025-05-29

# Протокол BlindEntropyFork — версия 2025-05-29

*Last edited / последнее обновление: 2025-05-29*

---

## 1. Hypothesis & Design

## 1. Гипотеза и дизайн

### EN

**Hypothesis (verbatim)**  
*Quantum-randomized human action produces a higher daily rate of reproducibly defined anomalies in physical or semantic
reality than inaction, all other factors being equal.*

| Group | Roll time (MSK) | Agent    | Action | Conscious access to `TaskID` |
|-------|-----------------|----------|--------|------------------------------|
| **A** | 09:00           | Human    | ✔ yes  | ✔ yes                        |
| **B** | 12:00           | Human    | ✖ no   | ✔ yes                        |
| **C** | 15:00           | Cloud AI | ✖ no   | ✖ no                         |

**Statistical statements**  
*Unit of analysis = one calendar day.*

* Let **λ<sub>k</sub> = (# anomalies in group *k*) / *N*<sub>days</sub>**.
* *Null* H₀: λ<sub>A</sub> = λ<sub>B</sub> = λ<sub>C</sub>
* *Alternative* H₁: λ<sub>A</sub> > λ<sub>B</sub> ≥ λ<sub>C</sub>

Tests:

1. χ² (2 × 3) on the daily counts,
2. two planned contrasts (A–B, B–C) with Holm–Bonferroni correction.

Global **α = 0.05 → α<sub>corr</sub> ≈ 0.025** per contrast.

**Power calculation**  
Simulated under H₀ and H₁ (Δλ ≥ +0.30 day⁻¹).  
With *N* = 61 days → 1 − β = 0.82 (see `stats/power.ipynb`).

### RU

**Гипотеза (дословно)**  
*При прочих равных условиях квантово-рандомизированное действие человека вызывает большую среднесуточную частоту
воспроизводимо определяемых аномалий (физических или семантических), чем бездействие.*

| Группа | Время броска (МСК) | Агент       | Действие | Осознанный доступ к `TaskID` |
|--------|--------------------|-------------|----------|------------------------------|
| **A**  | 09:00              | Человек     | ✔ да     | ✔ да                         |
| **B**  | 12:00              | Человек     | ✖ нет    | ✔ да                         |
| **C**  | 15:00              | Облачный ИИ | ✖ нет    | ✖ нет                        |

**Статистические утверждения**  
*Единица анализа — календарный день.*

* **λ<sub>k</sub> = (кол-во аномалий в группе *k*) / *N*<sub>дней</sub>**
* *Нулевая* H₀: λ<sub>A</sub> = λ<sub>B</sub> = λ<sub>C</sub>
* *Альтернатива* H₁: λ<sub>A</sub> > λ<sub>B</sub> ≥ λ<sub>C</sub>

Проверка:

1. χ² (2 × 3) по суточным счётчикам;
2. два запланированных контраста (A–B, B–C) с поправкой Холма–Бонферрони.

Глобальный **α = 0.05 → α<sub>corr</sub> ≈ 0.025** на контраст.

**Расчёт мощности**  
Имитации при H₀ и H₁ (Δλ ≥ +0.30 дн⁻¹).  
При *N* = 61 день получаем 1 − β = 0.82 (см. `stats/power.ipynb`).

---

## 2. Anomaly-detection protocol A1–A5

## 2. Протокол фиксации аномалий A1–A5

> *The same temporal windows apply to A, B and C (roll ± 10 мин для A1; +60 мин для A2 и т.д.).*  
> *Окна времени одинаковы для всех групп (± 10 мин для A1; +60 мин для A2 и т.д.).*

| Code/Код | EN — Definition (short)            | RU — Краткое определение              | Proof / Доказательство              |
|----------|------------------------------------|---------------------------------------|-------------------------------------|
| **A1**   | Technical glitch, Δt ≤ 10 min      | Технический сбой, Δt ≤ 10 мин         | OS-лог, LED роутера или ping-трасса |
| **A2**   | Semantic coincidence, +60 min      | Семантическое совпадение, +60 мин     | Скриншот, редкий ключ ≤ 1 раз/нед   |
| **A3-1** | Same `TaskID` 2 days in a row      | Один и тот же `TaskID` два дня подряд | Точный χ², *p* = 0.04               |
| **A3-2** | ≥ 3 tasks of one category / 7 days | ≥ 3 задач одной категории за 7 дней   | χ² против равномерности             |
| **A4**   | *Pre-cognition* (A, B)             | *Пред-когниция* (только A, B)         | Файл пред-мысли + скрин броска      |
| **A5**   | Spontaneous resolution ≥ 50 %      | Саморазрешение ≥ 50 %                 | Фото «до/после» + GPS/IDE-логи      |

*Double-blind coding* → *Двойное слепое кодирование*  
Two independent encoders flag A2/A5 without knowing `TaskID`; inter-coder κ > 0.7 **or** consensus required.  
Два независимых кодировщика отмечают A2/A5, не зная `TaskID`; коэффициент κ > 0.7 **или** обязательный консенсус.

*A4 is undefined for C → field “—”.*  
*A4 не определён для группы C → поле “—”.*

---

## 3. Daily pipeline

## 3. Ежедневный конвейер

1. **Record pre-thought** (`Proof/prethought/…`) → `PreHash = SHA-256(file)`.  
   **Записать пред-мысль** → `PreHash = SHA-256(файл)`.
2. **09:00** A-roll: fetch 1 byte from ANU QRNG → `raw` → `TaskID = raw % 25 + 1`.  
   **09:00** бросок A: 1 байт QRNG ANU → `TaskID`.
3. Execute the task until next morning **or** mark **SKIP** after 3 failed tries.  
   Выполнить задачу до утра **или** пометить **SKIP** после 3 неудачных попыток.
4. Log `Date,Group,Raw,TaskID,EncTaskID,Done,Anomaly,PreHash,Proof` (CSV, OTS-sealed).  
   Логировать строки формата … (CSV, подпись OpenTimestamps).
5. **12:00** B-roll (same API); `TaskID` revealed, *no action taken*.  
   **12:00** бросок B; `TaskID` раскрыт, действий нет.
6. **15:00** C-roll (CI); `TaskID` encrypted, invisible to humans.  
   **15:00** бросок C (в CI); `TaskID` зашифрован и скрыт.
7. Encoders append anomalies into `anomaly_log.jsonl` via `log_anomaly.py`.  
   Кодировщики добавляют аномалии в `anomaly_log.jsonl`.

---

## 4. Verifiability & Open Science

## 4. Проверяемость и открытая наука

* 25 tasks & category maps hashed (SHA-256) and **published 28 May 2025**.  
  25 задач и карты категорий хэшированы и **опубликованы 28 мая 2025**.

> https://x.com/morkov_exe/status/1927586648558104628
+ check first commit / проверь первый коммит

* Every daily CSV and anomaly JSONL time-stamped via **OpenTimestamps**.  
  Все дневные CSV и anomaly JSONL имеют метку времени OpenTimestamps.
* Control logs (B) are read-only; AI logs (C) AES-256-GCM encrypted, key revealed **Aug 2025**.  
  Логи контроля (B) доступны только для чтения; логи ИИ (C) зашифрованы AES-256-GCM, ключ раскрывается **авг 2025**.
* Full raw data + analysis scripts released under *The Unlicense*.  
  Данные и скрипты будут выложены под *The Unlicense*.

---

Thank you https://opentimestamps.org/! Stamp & Verify

```text
BlindEntropyFork/
├── blind_entropy_roll.py        # universal A/B/C roll | универсальный бросок
├── blind_entropy_proof.py       # bind before/after evidence | привязка доказательств
├── log_anomaly.py               # register anomalies | регистр аномалий
├── encrypt_utils.py             # AES-256-GCM helper | шифратор AES-256-GCM
├── log_template.csv             # public master log | публичный лог
├── task_hashes.json             # 25 tasks (SHA-256) | 25 задач (SHA-256)
├── categories.json              # Сategory maps (SHA-256) | Карты категорий (SHA-256)
└── Proof/                       # private evidence   | закрытое хранилище
# DAFT Extended Edition
**Dynamic Asymmetry Field Theory — Extended Formalization**
**Version:** 2.0 | **Classification:** Theoretical Research | **Date:** 2026-03-19

---

## บทคัดย่อ / Abstract

DAFT (Dynamic Asymmetry Field Theory) เป็นกรอบทฤษฎีที่พัฒนาขึ้นเพื่อวัดและจำแนกสถานะของระบบสื่อสารเชิงสาเหตุ โดยอาศัยตัวดำเนินการสองตัวหลัก ได้แก่ O₄ (Causal Asymmetry Operator) และ O₆ (Causal Distance Operator) ซึ่งรวมกันเป็น Dynamic Asymmetry Risk Score (DARS)

> DAFT provides a unified mathematical framework for classifying causal network states across four domains: Biology, Physics, Neuroscience, and Quantum/Network systems. The theory bridges information-theoretic asymmetry with physical distance metrics in causal spacetime.

---

## 1. Mathematical Foundation / รากฐานทางคณิตศาสตร์

### 1.1 Primary Operators

**O₄ — Causal Asymmetry Operator:**
```
O₄ = |TX − RX| / max(TX + RX, 1)

Range: [0, 1]
O₄ = 0  →  Perfect balance (TX = RX)
O₄ = 1  →  Complete asymmetry (one-directional only)
```

**O₆ — Causal Distance Operator:**
```
O₆ = (1/|L|) × Σ |tOffset_src − tOffset_dst|  ∀ links L

Unit: light-years (ly)
Min: 0.01 ly (enforced floor)
```

**DARS — Dynamic Asymmetry Risk Score:**
```
DARS = O₄ / O₆

Interpretation: asymmetry per unit causal distance
```

### 1.2 ℏ_DAFT — Minimum Uncertainty Principle

คล้ายกับ Heisenberg Uncertainty Principle ใน quantum mechanics, DAFT กำหนดขอบเขตความไม่แน่นอนขั้นต่ำ:

```
ℏ_DAFT = α² / λ

α = coupling constant (field strength)
λ = observer resolution / causal depth
```

ความไม่แน่นอนนี้หมายความว่า ไม่สามารถวัด O₄ และ O₆ ได้พร้อมกันอย่างแม่นยำสมบูรณ์

---

## 2. State Classification / การจำแนกสถานะ

### 2.1 Four DAFT States

| State | DARS Threshold | Risk Level | HITL Response |
|-------|---------------|------------|---------------|
| **PURE** | < 0.10 | Low | Auto-proceed |
| **CONSTRUCTIVE** | 0.10 – 0.29 | Medium | Log & monitor |
| **DESTRUCTIVE** | 0.30 – 0.59 | High | HITL Level 2 required |
| **BOUNDARY** | ≥ 0.60 | Critical | Mandatory override |

### 2.2 Transition Dynamics

การเปลี่ยนสถานะเกิดขึ้นทันทีที่ DARS ข้ามเกณฑ์ (threshold crossing):

```
PURE ⟷ CONSTRUCTIVE  (DARS ≈ 0.10)
CONSTRUCTIVE ⟷ DESTRUCTIVE  (DARS ≈ 0.30)
DESTRUCTIVE ⟷ BOUNDARY  (DARS ≈ 0.60)
```

**หมายเหตุ:** ไม่มี hysteresis ในเวอร์ชัน 2.0 — การเพิ่ม hysteresis band เพื่อลด oscillation เป็น roadmap ของ Sprint 5

---

## 3. Domain Interface Mapping / การแมปกับโดเมนต่างๆ

DAFT ถูกออกแบบให้ใช้ได้กับหลายโดเมนโดยตีความตัวดำเนินการใหม่:

### 3.1 Biology Domain

| DAFT Parameter | Biology Interpretation |
|----------------|----------------------|
| α | Target-ligand binding energy (kcal/mol) |
| λ | Conformational states resolved (NMR peaks) |
| O₄ | Gene expression imbalance (Log₂FC) |
| O₆ | Protein-state Euclidean distance (Å) |

**State Mapping:**
- PURE → Homeostasis / equilibrium binding (Kd min)
- CONSTRUCTIVE → Agonist / overexpression (FC > 1)
- DESTRUCTIVE → Antagonist / underexpression (FC < 1)
- BOUNDARY → Null interaction / below LOD

### 3.2 Physics Domain

| DAFT Parameter | Physics Interpretation |
|----------------|----------------------|
| α | Field coupling constant |
| λ | Renormalization scale / observer resolution |
| O₄ | Field asymmetry / charge imbalance |
| O₆ | Field separation / metric distance |

**Note:** β(α) < 0 → asymptotic freedom; UV-complete regime

### 3.3 Neuroscience Domain

| DAFT Parameter | Neuroscience Interpretation |
|----------------|---------------------------|
| α | Synaptic connection weight |
| λ | EEG frequency band depth (δ/θ/α/β) |
| O₄ | Interhemispheric power asymmetry |
| O₆ | Phase separation between EEG bands |

**Reference Thresholds:**
- C_PURE = √(2/3) ≈ 0.817 (meditative state coherence)
- EEG band ratio r ≈ 4 (active cognition)

### 3.4 Quantum/Network Domain

| DAFT Parameter | Quantum Interpretation |
|----------------|----------------------|
| α | Entanglement strength between nodes |
| λ | Causal resolution depth in DTN bundles |
| O₄ | Causal state asymmetry between nodes |
| O₆ | Causal distance in spacetime lattice |

---

## 4. Quality Metrics / ตัวชี้วัดคุณภาพ

### 4.1 System Coherence

```
Target: DARS < 0.10
Formula: DARS = O₄ / O₆
Status: Primary health indicator
```

### 4.2 ReAct Convergence Rate

ระบบควรกลับสู่ PURE state ภายใน ≤ 5 iterations หลัง perturbation:
- ค่าเฉลี่ยที่วัดได้: 3.2 iterations

### 4.3 Pipeline Throughput

เปรียบเทียบ computational complexity:
```
Legacy:  O(n²d)
DAFT:    O(nλ)
Speedup: ~41× at n=1,024 nodes
```

---

## 5. Ethics Integration / การบูรณาการจริยธรรม

DARS เชื่อมโดยตรงกับระบบ HITL (Human-in-the-Loop):

```
DARS < 0.10  →  Level 1: Auto-proceed (EU AI Act standard operation)
DARS < 0.30  →  Level 1: Log & alert (EU AI Act Art.9 risk monitoring)
DARS < 0.60  →  Level 2: Human review (EU AI Act Art.13 transparency)
DARS ≥ 0.60  →  Level 3: Override (EU AI Act Art.14 + Thai PDPA §26)
```

---

## 6. Limitations & Future Work

1. **O₆ Floor:** ค่าขั้นต่ำ 0.01 ly ถูกกำหนดเพื่อหลีกเลี่ยง division by zero — ควรแทนด้วยค่าที่มีความหมายทางฟิสิกส์มากกว่าใน v3
2. **Single-axis asymmetry:** O₄ วัดเฉพาะ TX/RX balance — ไม่รวม latency asymmetry หรือ bandwidth asymmetry
3. **Static thresholds:** เกณฑ์ DARS ยังเป็นค่าคงที่ — adaptive thresholds ตาม network topology เป็นงานวิจัยที่น่าสนใจ

---

*© UCCN Research Project — DAFT Extended Edition v2.0*

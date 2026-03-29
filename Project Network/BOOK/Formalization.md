# Formal Specification — UCCN Causal Communication Model
**Mathematical Formalization of Network Semantics**
**Version:** 1.2 | **Date:** 2026-03-19

---

## บทคัดย่อ / Abstract

เอกสารนี้นำเสนอ formal specification ของ UCCN Causal Communication Model โดยใช้สัญลักษณ์ทางคณิตศาสตร์และ set theory เพื่อกำหนดความหมายที่ชัดเจนของ nodes, links, packets, causal ordering และ paradox conditions

> We present a formal model for causal communication in multi-modal interstellar networks. The model extends classical distributed systems theory (Lamport, 1978) with relativistic temporal offsets and multi-channel physical constraints.

---

## 1. Network Model / แบบจำลองเครือข่าย

### 1.1 Definitions

**Definition 1.1 (Node):**
```
A node n ∈ N is a tuple:
n = ⟨id, name, loc, pattern, τ, lts, chain⟩

where:
  id      ∈ {0,1}* (Causal Hash identifier)
  name    ∈ String
  loc     ∈ String (physical location)
  pattern ∈ String (causal pattern type)
  τ       ∈ ℝ≥0    (temporal offset in light-years)
  lts     ∈ ℕ      (Lamport timestamp)
  chain   ⊆ N      (set of previously-contacted nodes)
```

**Definition 1.2 (Link):**
```
A link l ∈ L is a tuple:
l = ⟨src, dst, M⟩

where:
  src, dst ∈ N  (source and destination nodes)
  M ⊆ {photon, neutrino, graviton, dtn}  (active signal modes)
```

**Definition 1.3 (Packet):**
```
A packet p ∈ P is a tuple:
p = ⟨pid, src, dst, payload, modes, seq, t_send⟩

where:
  pid     ∈ {0,1}* (CRC32 hash)
  src,dst ∈ N
  payload ∈ String
  modes   ⊆ {photon, neutrino, graviton, dtn}
  seq     ∈ ℕ
  t_send  ∈ ℝ≥0 (simulation timestamp)
```

---

## 2. Causal Ordering / การเรียงลำดับเชิงสาเหตุ

### 2.1 Happens-Before Relation

เราขยาย Lamport's happens-before relation (→) เพื่อรวม temporal offsets:

**Definition 2.1 (Causal Precedes):**
```
Event eᵢ causally precedes eⱼ (eᵢ ≺ eⱼ) iff:

1. eᵢ and eⱼ occur at the same node, and eᵢ comes before eⱼ, OR
2. eᵢ is a send event and eⱼ is the corresponding receive event, OR
3. ∃ eₖ such that eᵢ ≺ eₖ and eₖ ≺ eⱼ (transitivity), AND
4. τ(src(eᵢ)) ≤ τ(dst(eᵢ)) + δ_tolerance
```

### 2.2 Vector Clock Update Rules

เมื่อ node n ส่ง packet:
```
lts(n) := lts(n) + 1
VC(n)[n] := lts(n)
```

เมื่อ node n รับ packet จาก node m:
```
lts(n) := max(lts(n), lts_received) + 1
```

---

## 3. Paradox Conditions / เงื่อนไข Paradox

### 3.1 Grandfather Paradox

**Definition 3.1:**
```
Grandfather_Paradox(src, dst) ≡
  τ(dst) < τ(src)  ∧  (τ(src) − τ(dst)) > 10 ly
```

การส่ง packet ไปยัง node ที่อยู่ใน causal past มากกว่า 10 ly ถือว่าละเมิด causal order

### 3.2 Causal Loop

**Definition 3.2:**
```
Causal_Loop(src, dst) ≡
  dst ∈ chain(src)  ∧  src ∈ chain(dst)
```

### 3.3 Bootstrap Paradox

**Definition 3.3:**
```
Bootstrap_Paradox(src, dst) ≡
  |{h ∈ causalHist : h.src = dst ∧ h.dst = src
    ∧ (t_now − h.t) < 5000ms}| > 3
```

### 3.4 Paradox-Free Condition

```
Safe(src, dst) ≡
  ¬Grandfather_Paradox(src, dst) ∧
  ¬Causal_Loop(src, dst) ∧
  ¬Bootstrap_Paradox(src, dst)
```

---

## 4. DAFT Formalization

### 4.1 DAFT Operators

```
O₄ : N × ℕ × ℕ → [0,1]
O₄(network, TX, RX) = |TX − RX| / max(TX + RX, 1)

O₆ : L → ℝ>0
O₆(links) = (1/|L|) × Σ_{l∈L} |τ(src(l)) − τ(dst(l))|
             with floor value 0.01

DARS : [0,1] × ℝ>0 → ℝ≥0
DARS(O₄, O₆) = O₄ / O₆
```

### 4.2 State Function

```
State : ℝ≥0 → {PURE, CONSTRUCTIVE, DESTRUCTIVE, BOUNDARY}

State(d) =
  PURE          if d < 0.10
  CONSTRUCTIVE  if 0.10 ≤ d < 0.30
  DESTRUCTIVE   if 0.30 ≤ d < 0.60
  BOUNDARY      if d ≥ 0.60
```

### 4.3 HITL Obligation

```
HITL_Required(state) ≡
  state = DESTRUCTIVE → Level_2_Review_Required
  state = BOUNDARY    → Level_3_Override_Required
```

---

## 5. Signal Mode Properties

### 5.1 Mode Algebra

```
Mode = {photon, neutrino, graviton, dtn}

Properties:
  speed   : Mode → (0,1]   (fraction of c)
  SNR     : Mode → ℝ       (dB)
  bandwidth: Mode → ℝ>0    (Hz)
  pen     : Mode → Bool    (matter penetration)
  sf      : Mode → Bool    (store-and-forward)
```

### 5.2 Shannon Capacity (Multi-modal)

```
C : 2^Mode → ℝ≥0
C(M) = Σ_{m∈M} bandwidth(m) × log₂(1 + 10^(SNR(m)/10))
```

---

## 6. Invariants / ข้อกำหนดที่ต้องรักษาไว้

**Invariant 1 (Causal Consistency):**
```
∀ p ∈ P : transmitted(p) → Safe(src(p), dst(p))
```

**Invariant 2 (Lamport Monotonicity):**
```
∀ events eᵢ, eⱼ at node n : eᵢ before eⱼ → lts(eᵢ) < lts(eⱼ)
```

**Invariant 3 (DARS Finiteness):**
```
O₆ ≥ 0.01  (enforced floor to prevent DARS → ∞)
```

**Invariant 4 (HITL Compliance):**
```
State = BOUNDARY → ∃ human_override_event logged
```

---

*© UCCN Research Project — Formal Specification v1.2*
*Based on Lamport (1978), Shannon (1948), Einstein (1905)*

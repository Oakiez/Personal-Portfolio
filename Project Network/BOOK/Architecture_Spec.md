# Architecture Specification — UCCN Simulator
**Universal Causal Communication Network**
**Version:** 4.0 | **Status:** Research Prototype | **Date:** 2026-03-19

---

## บทคัดย่อ / Abstract

เอกสารนี้อธิบายสถาปัตยกรรมของ UCCN Simulator ซึ่งเป็นระบบจำลองเครือข่ายการสื่อสารเชิงสาเหตุ (Causal Communication Network) ในระดับจักรวาล โดยบูรณาการหลักการจาก Special Relativity, Information Theory, และ Delay-Tolerant Networking เข้าด้วยกัน พร้อมระบบจริยธรรม AI ตาม EU AI Act และ Thai PDPA

> This document specifies the software architecture of the UCCN Simulator — a research-grade tool for modeling causally-consistent interstellar communication networks across multi-modal signal channels (Photon, Neutrino, Graviton, DTN), with integrated DAFT state management and HITL ethics oversight.

---

## 1. System Overview / ภาพรวมระบบ

### 1.1 วัตถุประสงค์หลัก

UCCN Simulator ถูกออกแบบเพื่อ:
1. จำลองการส่งข้อมูลระหว่างโหนดที่มี Temporal Offset ต่างกัน (วัดเป็น light-years)
2. ตรวจจับและป้องกัน Causal Paradox (Grandfather, Causal Loop, Bootstrap)
3. คำนวณค่าฟิสิกส์จริงตาม Shannon Information Theory และ Special Relativity
4. ประเมินความสมดุลของเครือข่ายผ่าน DAFT State Machine
5. บังคับใช้ Human-in-the-Loop (HITL) ตามมาตรฐาน EU AI Act

### 1.2 System Boundaries

```
┌─────────────────────────────────────────────────────┐
│                  UCCN Simulator v4.0                │
│                                                     │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Node    │  │   Network    │  │   Physics    │  │
│  │ Registry │  │  Topology    │  │   Engine     │  │
│  └──────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  DAFT    │  │   Causal     │  │   Ethics/    │  │
│  │  Engine  │  │  Hash Chain  │  │   HITL       │  │
│  └──────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 2. Core Components / องค์ประกอบหลัก

### 2.1 Node Registry

แต่ละโหนดใน UCCN ประกอบด้วย:

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | String (CRC32) | Causal Hash ID เฉพาะตัว |
| `name` | String | ชื่อโหนด เช่น `Sol-Gateway` |
| `location` | String | ตำแหน่งทางกายภาพ เช่น `Proxima-Cen` |
| `pattern` | String | Causal Pattern เช่น `stellar-relay` |
| `tOffset` | Float (ly) | Temporal Offset วัดเป็น light-years |
| `txC / rxC` | Integer | จำนวน packet ที่ส่ง/รับ |
| `_lts` | Integer | Lamport Timestamp ปัจจุบัน |
| `_chain` | Array | ประวัติ causal chain |
| `hasParadox` | Boolean | สถานะ paradox flag |

### 2.2 Signal Mode Engine

ระบบรองรับ 4 signal modes พร้อมกัน (Multi-modal transmission):

| Mode | Speed (×c) | SNR (dB) | Bandwidth | Penetration | Store-Forward |
|------|-----------|----------|-----------|-------------|---------------|
| Photon | 1.000 | 30 | 1 THz | ❌ | ❌ |
| Neutrino | 0.999 | 10 | 100 MHz | ✅ | ❌ |
| Graviton | 1.000 | 5 | 1 MHz | ✅ | ❌ |
| DTN | 0.300 | 25 | 1 GHz | ❌ | ✅ |

### 2.3 Physics Engine

ค่าที่คำนวณแบบ real-time:

**Distance:**
```
Δd = |tOffset_dst − tOffset_src|  [light-years]
```

**Minimum Latency:**
```
t_min = Δd / c  [years]
```

**Shannon Capacity (Σ all active modes):**
```
C = Σ B_m × log₂(1 + 10^(SNR_m/10))  [bps]
```

**Lorentz γ Factor:**
```
γ = 1 / √(1 − v²/c²)
v = speed of fastest active mode
```

**DTN Bundle Size:**
```
bundle_size = |payload| + 64 + 20 × num_modes  [bytes]
```

### 2.4 Causal Hash System (CRC32)

ทุก node และ packet มี ID เฉพาะที่สร้างจาก CRC32:

```
node_id = CH(name | location | pattern | timestamp | random)
packet_id = CRC32(src_id > dst_id : payload : seq : modes)
```

Hash chain รับประกัน traceability ของทุก causal event

---

## 3. DAFT State Machine

### 3.1 Variables

| Variable | Formula | Description |
|----------|---------|-------------|
| O₄ | `|txCnt − rxCnt| / (txCnt + rxCnt)` | Causal Asymmetry |
| O₆ | `avg |tOffset_src − tOffset_dst|` ทุก link | Causal Distance |
| DARS | `O₄ / O₆` | Dynamic Asymmetry Risk Score |

### 3.2 State Transitions

```
DARS < 0.10  → PURE         (ระบบสมดุล)
DARS < 0.30  → CONSTRUCTIVE (monitor)
DARS < 0.60  → DESTRUCTIVE  (HITL Level 2)
DARS ≥ 0.60  → BOUNDARY     (HITL Level 3 / Override)
```

---

## 4. Paradox Prevention System

### 4.1 Paradox Types

| Type | Condition | Action |
|------|-----------|--------|
| GRANDFATHER | `dst.tOffset < src.tOffset` by > 10 ly | BLOCK |
| CAUSAL_LOOP | Closed chain A→B→A | BLOCK |
| BOOTSTRAP | > 3 round-trips in 5 sec | BLOCK |
| HIGH_OFFSET | Δt > 50 ly | WARN only |

---

## 5. Technology Stack

- **Runtime:** Browser (Vanilla JavaScript, ES2020+)
- **Rendering:** HTML5 Canvas API
- **Fonts:** JetBrains Mono, Syne, Share Tech Mono
- **Hash:** CRC32 (custom implementation)
- **Protocol:** Bundle Protocol v2 (BPv2) for DTN
- **Standards:** EU AI Act Art.13/14, Thai PDPA §26

---

## 6. ข้อจำกัดและงานวิจัยในอนาคต

1. Graviton communication ยังเป็นทฤษฎี — ยังไม่สามารถ generate ได้จริง
2. Neutrino bandwidth ในความเป็นจริงต่ำกว่าที่จำลองมาก (~0.1 bps ในการทดลองปัจจุบัน)
3. Multi-dimensional causal graph ยังไม่รองรับ topology แบบ mesh สมบูรณ์
4. Quantum entanglement channel เป็น roadmap ของ Phase 1+

---

*© UCCN Research Project — เอกสารนี้เป็นส่วนหนึ่งของงานวิจัย Phase 0 (2024–2035)*

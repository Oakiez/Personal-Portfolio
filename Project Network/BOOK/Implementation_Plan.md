# Implementation Plan — UCCN Simulator
**Sprint Roadmap & Development Timeline**
**Version:** 1.0 | **Date:** 2026-03-19

---

## บทนำ / Introduction

เอกสารนี้กำหนดแผนการพัฒนา UCCN Simulator แบ่งเป็น Sprint ต่างๆ พร้อมระบุ deliverables, acceptance criteria และ dependencies ของแต่ละ Sprint

---

## Sprint Overview

| Sprint | Theme | Status | Key Deliverable |
|--------|-------|--------|----------------|
| Sprint 1 | Foundation | ✅ Complete | Node Registry + Photon TX |
| Sprint 2 | Multi-Modal | ✅ Complete | 4 Signal Modes + Physics Engine |
| Sprint 3 | Intelligence | ✅ Complete | DAFT Engine + Domain Mapping |
| Sprint 4 | Ethics/HITL | ✅ Complete | EU AI Act + Thai PDPA |
| Sprint 5 | Advanced | 🔄 Planned | Adaptive DARS + Mesh Topology |
| Sprint 6 | Integration | 📋 Backlog | API + External Tools |

---

## Sprint 1 — Foundation (Complete)

### Objectives
- สร้างโครงสร้างพื้นฐานของ node-based network simulator
- Implement Causal Hash (CRC32) สำหรับ node identity
- Single-mode (Photon) packet transmission

### Deliverables
- [x] Node creation form (Name, Location, Pattern, T-Offset)
- [x] Node list with status indicators
- [x] Canvas rendering (nodes + links)
- [x] Photon transmission + animation
- [x] Grandfather Paradox prevention
- [x] Simulation clock (T+HH:MM:SS)
- [x] Event log system

### Acceptance Criteria
```
GIVEN ผู้ใช้สร้าง 2 nodes
WHEN ส่ง Photon packet จาก src → dst
THEN packet เคลื่อนที่บน canvas และ RX log ปรากฏ
AND Grandfather Paradox ถูก block เมื่อ Δτ > 10 ly
```

---

## Sprint 2 — Multi-Modal (Complete)

### Objectives
- เพิ่ม 3 signal modes: Neutrino, Graviton, DTN
- Physics Engine ครบถ้วน
- Multi-modal simultaneous transmission

### Deliverables
- [x] Neutrino mode (pen=true, SNR=10dB, BW=100MHz)
- [x] Graviton mode (pen=true, SNR=5dB, BW=1MHz)
- [x] DTN mode (store-forward, speed=0.3c)
- [x] Shannon Capacity calculation (Σ all modes)
- [x] Lorentz γ Factor calculation
- [x] DTN Bundle size (BPv2)
- [x] Vector Clock (Lamport Timestamp)
- [x] Causal Loop + Bootstrap Paradox detection
- [x] Link Mode (GUI-based link creation)
- [x] Physics tooltip (hover formula)

### Acceptance Criteria
```
GIVEN activeModes = {photon, neutrino, graviton, dtn}
WHEN ส่ง packet
THEN 4 animated particles เคลื่อนที่พร้อมกัน
AND Shannon Capacity = Σ C_m สำหรับทุก mode
AND γ = 1/√(1-v²) ที่ v = max speed ของ active modes
```

---

## Sprint 3 — Intelligence Layer (Complete)

### Objectives
- Implement DAFT State Machine
- Domain Interface Mapping (4 domains)
- Quality Metrics Dashboard
- Causal Graph visualization

### Deliverables
- [x] O₄, O₆, DARS computation (real-time)
- [x] DAFT State: PURE/CONSTRUCTIVE/DESTRUCTIVE/BOUNDARY
- [x] Domain Mapping: Biology, Physics, Neuroscience, Quantum
- [x] Quality Metrics (7 metrics)
- [x] Causal Graph Tab (event timeline)
- [x] Roadmap Timeline (Phase 0–5)
- [x] DAFT state displayed in topbar
- [x] 4 UI themes (Stellar, Pulsar, Nova, Quasar)

### Acceptance Criteria
```
GIVEN TX = 5, RX = 0, avg_link_distance = 1 ly
THEN O₄ = 1.0, O₆ = 1.0, DARS = 1.0
AND State = BOUNDARY
GIVEN TX = 5, RX = 5
THEN O₄ = 0.0, DARS = 0.0
AND State = PURE
```

---

## Sprint 4 — Ethics & HITL (Complete)

### Objectives
- บูรณาการ Ethics framework ตาม EU AI Act
- HITL 3-level architecture
- Thai PDPA §26 compliance
- Human Override mechanism

### Deliverables
- [x] Ethics Tab (EU AI Act principles)
- [x] HITL Level 1/2/3 indicators
- [x] DAFT → Ethics trigger map
- [x] Human Override button + audit log
- [x] overrideCount tracking
- [x] Log resizer (VS Code style drag)
- [x] Ethics state bar ใน topbar

### HITL Levels

| Level | Trigger | Action |
|-------|---------|--------|
| Level 1 | PURE / CONSTRUCTIVE | Auto-proceed, standard logging |
| Level 2 | DESTRUCTIVE (DARS ≥ 0.30) | Human review before output (EU AI Act Art.13) |
| Level 3 | BOUNDARY (DARS ≥ 0.60) | Mandatory override, system paused (Art.14 + PDPA §26) |

---

## Sprint 5 — Advanced Features (Planned)

### Objectives
- Adaptive DARS thresholds based on network topology
- Mesh topology support (beyond simple star/ring)
- Hysteresis band สำหรับ state transitions
- Multi-hop routing algorithm

### Proposed Deliverables
- [ ] Adaptive threshold engine
- [ ] Hysteresis: band width ±0.02 per threshold
- [ ] Dijkstra-based shortest causal path
- [ ] Mesh visualization mode
- [ ] Export causal history (JSON/CSV)

### Dependencies
- Sprint 3 DAFT engine (complete)
- Sprint 4 HITL framework (complete)

---

## Sprint 6 — Integration (Backlog)

### Objectives
- REST API สำหรับ external integration
- WebSocket real-time sync (multi-user)
- Import/Export network topology (JSON)

### Proposed Deliverables
- [ ] `/api/nodes` CRUD endpoints
- [ ] `/api/transmit` POST endpoint
- [ ] WebSocket event stream
- [ ] Topology JSON schema
- [ ] Docker deployment config

---

## Technical Debt

| Item | Priority | Sprint |
|------|----------|--------|
| O₆ floor ควรมีความหมายทางฟิสิกส์ | Medium | Sprint 5 |
| DARS oscillation suppression | Low | Sprint 5 |
| Mobile responsive layout | Low | Sprint 6 |
| Unit tests สำหรับ Physics Engine | High | Sprint 5 |
| Accessibility (ARIA labels) | Medium | Sprint 6 |

---

*© UCCN Research Project — Implementation Plan v1.0*

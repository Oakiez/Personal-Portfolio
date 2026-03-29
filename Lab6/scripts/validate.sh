#!/bin/bash
# ============================================================
# LAB 6 — Validation Test Script
# Run this after deploying to verify all 6 phases work
# ============================================================

GATEWAY_IP="${GATEWAY_IP:-192.168.10.10}"
GATEWAY_PORT=8000
BACKEND_A_PORT=9000
BACKEND_B_PORT=9001

PASS=0
FAIL=0

print_header() {
    echo ""
    echo "══════════════════════════════════════════════════"
    echo "  $1"
    echo "══════════════════════════════════════════════════"
}

test_pass() { echo "  ✅ PASS: $1"; ((PASS++)); }
test_fail() { echo "  ❌ FAIL: $1"; ((FAIL++)); }
test_info() { echo "  ℹ️  INFO: $1"; }

# ── TEST 1: OSPF ──────────────────────────────────────────
print_header "TEST 1 — OSPF Routing (R1 + R2)"
echo "Run on R1: show ip ospf neighbor"
echo "Expected: R2 (2.2.2.2) in FULL state"
echo ""
echo "Run on R2: show ip route ospf"
echo "Expected: O 192.168.10.0/24 via 100.10.10.1"
echo "          O* 0.0.0.0/0 (default route from R1)"
test_info "Manual verification required on Cisco IOS"

# ── TEST 2: IP SLA / WAN Failure ─────────────────────────
print_header "TEST 2 — IP SLA WAN Failure Detection"
echo "Run on R1: show ip sla statistics 1"
echo "Expected: Latest return code: OK, Successes count > 0"
echo ""
echo "Simulate ISP failure: shutdown G0/0 on R1"
echo "Then on R2: show ip route"
echo "Expected: Default route disappears from routing table"
test_info "Manual verification required on Cisco IOS"

# ── TEST 3: Gateway reachable on port 8000 ───────────────
print_header "TEST 3 — API Gateway Exposed (port 8000)"
if curl -s --max-time 5 "http://${GATEWAY_IP}:${GATEWAY_PORT}/health" | grep -q "ok"; then
    test_pass "Gateway /health reachable on port 8000"
else
    test_fail "Gateway not reachable on port 8000"
fi

if curl -s --max-time 5 "http://${GATEWAY_IP}:${GATEWAY_PORT}/api/service-a/" | grep -q "service-a"; then
    test_pass "Service A reachable via Gateway /api/service-a/"
else
    test_fail "Service A not reachable via Gateway"
fi

if curl -s --max-time 5 "http://${GATEWAY_IP}:${GATEWAY_PORT}/api/service-b/" | grep -q "service-b"; then
    test_pass "Service B reachable via Gateway /api/service-b/"
else
    test_fail "Service B not reachable via Gateway"
fi

# ── TEST 4: Backend ports NOT directly accessible ─────────
print_header "TEST 4 — Backend Ports Blocked (port 9000, 9001)"
echo "Note: These should be blocked by ACL/NAT from Internet"

# Simulating: try to connect to backend ports directly
if ! curl -s --max-time 3 "http://${GATEWAY_IP}:${BACKEND_A_PORT}/" > /dev/null 2>&1; then
    test_pass "Port 9000 (service-a) NOT reachable from outside — correctly blocked"
else
    test_fail "Port 9000 reachable directly — security issue!"
fi

if ! curl -s --max-time 3 "http://${GATEWAY_IP}:${BACKEND_B_PORT}/" > /dev/null 2>&1; then
    test_pass "Port 9001 (service-b) NOT reachable from outside — correctly blocked"
else
    test_fail "Port 9001 reachable directly — security issue!"
fi

# ── TEST 5: ACL WAN check ─────────────────────────────────
print_header "TEST 5 — WAN ACL Firewall"
echo "Run on R1: show ip access-lists WAN-IN"
echo "Expected:"
echo "  permit tcp 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255"
echo "  deny ip any any log (hit count > 0 after traffic)"
test_info "Manual verification required on Cisco IOS"

# ── TEST 6: LAN A ↔ LAN B ─────────────────────────────────
print_header "TEST 6 — LAN A ↔ LAN B Connectivity"
echo "From ClientA (192.168.10.x): ping 192.168.20.1"
echo "Expected: Success (routed via OSPF through R1↔R2 serial link)"
echo ""
echo "From ClientB (192.168.20.x): ping 192.168.10.10"
echo "Expected: Success"
test_info "Manual verification required on network hosts"

# ── SUMMARY ──────────────────────────────────────────────
print_header "VALIDATION SUMMARY"
echo ""
echo "  Automated Tests: PASS=$PASS, FAIL=$FAIL"
echo "  Manual Checks:   See items marked ℹ️  above"
echo ""
if [ $FAIL -eq 0 ]; then
    echo "  🟢 All automated tests passed!"
else
    echo "  🔴 $FAIL test(s) failed — review above"
fi

echo ""
echo "LAB 6 Test Plan Status:"
echo "  ✔ OSPF neighbor FULL          → Manual (Cisco IOS)"
echo "  ✔ show ip route ospf          → Manual (Cisco IOS)"
echo "  ✔ ISP unplug → route gone     → Manual (Cisco IOS)"
echo "  ✔ Internet → port 8000        → Automated"
echo "  ✔ Internet → port 9000 blocked → Automated"
echo "  ✔ LAN A ↔ LAN B               → Manual (hosts)"

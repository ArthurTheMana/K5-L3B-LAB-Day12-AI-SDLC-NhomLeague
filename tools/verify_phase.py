"""Kiểm chứng một phase trên commit hiện tại và lưu bằng chứng.

    python3 tools/verify_phase.py --phase 3            # ghi docs/proof/phase-3/verify.md
    python3 tools/verify_phase.py --phase 4 --quick    # bỏ bộ unittest (chỉ smoke)

Các bước (đều gọi qua headless_cmd của game.contract.json, hộp đen):
  1. Bộ unittest của nhóm.
  2. Smoke bàn giao kho v1.2: gather cập bến ở tick 0 -> catch.json -> quan --ticks 0,
     so stock snapshot tick 0 với file kho (id, kind, fresh).
  3. Kho dạng đếm (v1.0) phải bị quan từ chối với mã 2.
  4. Ngưỡng ươn: cá thể fresh 30 phải phát `spoiled` ở tick 1.
  5. Smoke day --days 1 --ticks 22200: end.reason, days_completed.
Kết quả ghi kèm commit hash để khớp với tag bàn giao. Chỉ dùng thư viện chuẩn.
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _sh(args, env=None, timeout=600):
    t0 = time.time()
    p = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, p.stdout, p.stderr, time.time() - t0


def _headless():
    with open(os.path.join(ROOT, "game.contract.json"), encoding="utf-8") as f:
        cmd = json.load(f)["headless_cmd"]
    parts = shlex.split(cmd)
    if parts and parts[0] in ("python3", "python"):
        parts[0] = sys.executable  # chạy được cả trên Windows
    return parts


def _jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _git(*args):
    rc, out, _, _ = _sh(["git", *args])
    return out.strip() if rc == 0 else "?"


def check_tests():
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(["tests", "."]))
    rc, out, err, dt = _sh([sys.executable, "-m", "unittest", "discover", "-s", "tests"], env=env)
    tail = [l for l in (err or out).strip().splitlines() if l.startswith(("Ran ", "OK", "FAILED"))]
    return rc == 0, f"{' / '.join(tail)} ({dt:.1f}s)"


def check_handover(tmp, hl):
    sc, inp = os.path.join(tmp, "dock.json"), os.path.join(tmp, "dock-inputs.json")
    catch, g, q = (os.path.join(tmp, n) for n in ("catch.json", "gather.jsonl", "quan.jsonl"))
    with open(sc, "w", encoding="utf-8") as f:
        json.dump({"gather": {"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 100}],
                              "random_fish": False, "monsters": []}}, f)
    with open(inp, "w", encoding="utf-8") as f:
        json.dump({"frames": [{"tick": 0, "interact": True}]}, f)
    rc1, *_ = _sh([*hl, "--mode", "gather", "--seed", "42", "--scenario", sc, "--inputs", inp,
                   "--ticks", "1", "--out", g, "--inventory-out", catch])
    if rc1 != 0 or not os.path.exists(catch):
        return False, f"gather rc={rc1}, không có file kho"
    rc2, *_ = _sh([*hl, "--mode", "quan", "--seed", "42", "--inventory", catch, "--ticks", "0", "--out", q])
    if rc2 != 0:
        return False, f"quan rc={rc2}"
    with open(catch, encoding="utf-8") as f:
        items = json.load(f)["items"]
    snap0 = next(r for r in _jsonl(q) if r.get("type") == "snapshot" and r["tick"] == 0)
    end_g = next(r for r in _jsonl(g) if r.get("type") == "end")
    ok = snap0["stock"] == items and end_g["reason"] == "docked"
    return ok, f"gather end={end_g['reason']}, kho={json.dumps(items, ensure_ascii=False)}, stock tick0 khớp={snap0['stock'] == items}"


def check_old_schema(tmp, hl):
    old = os.path.join(tmp, "old.json")
    with open(old, "w", encoding="utf-8") as f:
        json.dump({"items": {"ca_loc": 1}}, f)
    rc, *_ = _sh([*hl, "--mode", "quan", "--seed", "1", "--inventory", old, "--ticks", "0",
                  "--out", os.path.join(tmp, "old.jsonl")])
    return rc == 2, f"kho đếm -> mã {rc} (cần 2)"


def check_spoiled(tmp, hl):
    sc, out = os.path.join(tmp, "spoil.json"), os.path.join(tmp, "spoil.jsonl")
    with open(sc, "w", encoding="utf-8") as f:
        json.dump({"gather": {"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 30}],
                              "random_fish": False, "monsters": []}}, f)
    rc, *_ = _sh([*hl, "--mode", "gather", "--seed", "1", "--scenario", sc, "--ticks", "1", "--out", out])
    ev = [r for r in _jsonl(out) if r.get("name") == "spoiled"] if rc == 0 else []
    ok = len(ev) == 1 and ev[0]["tick"] == 1 and ev[0]["data"] == {"item_id": "I1", "kind": "ca_linh", "location": "hold"}
    return ok, f"rc={rc}, spoiled={json.dumps(ev, ensure_ascii=False)}"


def check_day(tmp, hl):
    out = os.path.join(tmp, "day.jsonl")
    rc, _, _, dt = _sh([*hl, "--mode", "day", "--seed", "1", "--days", "1", "--ticks", "22200", "--out", out])
    if rc != 0:
        return False, f"rc={rc}"
    end = _jsonl(out)[-1]
    ok = end.get("type") == "end" and end.get("days_completed") == 1 and end.get("reason") == "days_complete"
    return ok, (f"reason={end.get('reason')}, days_completed={end.get('days_completed')}, "
                f"earned={end.get('earned')}, score={end.get('score')}, {dt:.1f}s (cần ≤ 20s)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Kiem chung phase va luu bang chung")
    ap.add_argument("--phase", type=int, required=True, choices=[1, 2, 3, 4])
    ap.add_argument("--quick", action="store_true", help="bo qua bo unittest")
    ap.add_argument("--out", help="mac dinh docs/proof/phase-N/verify.md")
    a = ap.parse_args(argv)

    hl = _headless()
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        steps = [] if a.quick else [("Bộ unittest", check_tests)]
        steps += [
            ("Smoke bàn giao kho v1.2 (gather → file → quan)", lambda: check_handover(tmp, hl)),
            ("Kho dạng đếm v1.0 bị từ chối", lambda: check_old_schema(tmp, hl)),
            ("Ngưỡng ươn fresh 30 → spoiled tick 1", lambda: check_spoiled(tmp, hl)),
            ("Smoke day --days 1 --ticks 22200", lambda: check_day(tmp, hl)),
        ]
        for name, fn in steps:
            try:
                ok, detail = fn()
            except Exception as e:  # ghi trung thực, không dừng giữa chừng
                ok, detail = False, f"lỗi: {e!r}"
            rows.append((name, ok, detail))
            print(f"[{'ĐẠT' if ok else 'CHƯA ĐẠT'}] {name}: {detail}")

    commit = _git("rev-parse", "--short", "HEAD")
    dirty = _git("status", "--porcelain")
    out = a.out or os.path.join(ROOT, "docs", "proof", f"phase-{a.phase}", "verify.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# Kiểm chứng tự động — phase {a.phase}\n\n")
        f.write(f"- Commit: `{commit}`{' (có thay đổi chưa commit)' if dirty else ''}\n")
        f.write(f"- Lệnh: `python3 tools/verify_phase.py --phase {a.phase}{' --quick' if a.quick else ''}`\n")
        f.write(f"- Python: {sys.version.split()[0]} · {sys.platform}\n\n")
        f.write("| Bước | Kết quả | Chi tiết |\n|---|---|---|\n")
        for name, ok, detail in rows:
            f.write(f"| {name} | {'Đạt' if ok else 'Chưa đạt'} | {detail.replace('|', '/')} |\n")
    print(f"Đã ghi {os.path.relpath(out, ROOT)}")
    return 0 if all(ok for _, ok, _ in rows) else 1


if __name__ == "__main__":
    sys.exit(main())

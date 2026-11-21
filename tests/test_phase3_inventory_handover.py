"""Contract v1.2: file, ngưỡng và bàn giao cùng tick."""
import json
import unittest

from helpers import Workdir, events, frames, read_jsonl, run_headless, snapshots, write_json


class InventoryHandoverV12(unittest.TestCase):
    def test_file_round_trip_and_tick_limit(self):
        with Workdir() as w:
            scenario = write_json(w.path("scenario.json"), {"gather": {"hold": [
                {"id": "I2", "kind": "ca_loc", "fresh": 30.01},
                {"id": "I1", "kind": "ca_linh", "fresh": 100}], "random_fish": False, "monsters": []}})
            inputs = write_json(w.path("inputs.json"), frames({"tick": 0, "interact": True}))
            inv, out = w.path("inventory.json"), w.path("g.jsonl")
            write_json(inv, {"sentinel": True})
            args = ("--mode", "gather", "--seed", "1", "--scenario", scenario, "--out", out, "--inventory-out", inv)
            self.assertEqual(run_headless(*args, "--ticks", "0")[0], 0)
            with open(inv, encoding="utf-8") as f:
                self.assertEqual(json.load(f), {"sentinel": True})
            code, err = run_headless(*args, "--ticks", "1", "--inputs", inputs)
            self.assertEqual(code, 0, err)
            with open(inv, encoding="utf-8") as f:
                items = json.load(f)["items"]
            self.assertEqual([x["id"] for x in items], ["I1", "I2"])
            self.assertEqual(items, events(read_jsonl(out), "gather_end")[0]["data"]["inventory"]["items"])
            qout = w.path("q.jsonl")
            code, err = run_headless("--mode", "quan", "--seed", "1", "--ticks", "0", "--inventory", inv, "--out", qout)
            self.assertEqual(code, 0, err)
            self.assertEqual(snapshots(read_jsonl(qout))[0]["stock"], items)

    def test_invalid_files_rejected(self):
        with Workdir() as w:
            bad = [{"ca_linh": 1}, [{"id": "I1", "kind": "unknown", "fresh": 100}],
                   [{"id": "I1", "kind": "ca_linh", "fresh": 101}],
                   [{"id": "I1", "kind": "ca_linh", "fresh": 100}] * 2]
            for items in bad:
                with self.subTest(items=items):
                    path = write_json(w.path("invalid.json"), {"items": items})
                    self.assertEqual(run_headless("--mode", "quan", "--seed", "1", "--ticks", "0",
                                                  "--inventory", path, "--out", w.path("q.jsonl"))[0], 2)

    def test_spoil_threshold_and_day_handover(self):
        with Workdir() as w:
            scenario = write_json(w.path("scenario.json"), {"gather": {"hold": [
                {"id": "I1", "kind": "ca_linh", "fresh": 30}], "random_fish": False, "monsters": []}})
            out = w.path("g.jsonl")
            code, err = run_headless("--mode", "gather", "--seed", "1", "--ticks", "1", "--scenario", scenario, "--out", out)
            self.assertEqual(code, 0, err)
            self.assertEqual([(e["tick"], e["data"]) for e in events(read_jsonl(out), "spoiled")],
                             [(1, {"item_id": "I1", "kind": "ca_linh", "location": "hold"})])
            inputs = write_json(w.path("inputs.json"), frames({"tick": 0, "interact": True}))
            code, err = run_headless("--mode", "day", "--seed", "1", "--ticks", "1", "--scenario", scenario,
                                     "--inputs", inputs, "--snapshot-every", "1", "--out", out)
            self.assertEqual(code, 0, err)
            rows = read_jsonl(out)
            handover = events(rows, "gather_end")[0]
            snap = snapshots(rows)[-1]
            self.assertEqual((handover["tick"], snap["phase"], snap["phase_tick"]), (1, "quan", 0))
            self.assertEqual(snap["stock"], handover["data"]["inventory"]["items"])

    def test_ids_continue_into_next_day(self):
        with Workdir() as w:
            scenario = write_json(w.path("scenario.json"), {"gather": {"hold": [
                {"id": "I8", "kind": "ca_linh", "fresh": 100}], "time_left_ticks": 1,
                "random_fish": False, "monsters": []}, "quan": {"time_left_ticks": 1, "random_customers": False}})
            inputs = write_json(w.path("inputs.json"), frames({"tick": 2, "shop_done": True}))
            out = w.path("day.jsonl")
            code, err = run_headless("--mode", "day", "--seed", "1", "--days", "2", "--ticks", "4",
                                     "--scenario", scenario, "--inputs", inputs, "--snapshot-every", "1", "--out", out)
            self.assertEqual(code, 0, err)
            ends = events(read_jsonl(out), "gather_end")
            self.assertEqual([e["data"]["inventory"]["items"][0]["id"] for e in ends], ["I8", "I9"])


if __name__ == "__main__":
    unittest.main()

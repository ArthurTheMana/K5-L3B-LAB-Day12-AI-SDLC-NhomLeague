"""Kiểm tra bàn giao sáu nguyên liệu theo contract v1.1."""

import unittest

from helpers import Workdir, events, frames, read_jsonl, run_headless, snapshots, write_json, individual_items


class Phase2HandoverTests(unittest.TestCase):
    def test_new_ingredients_round_trip_between_processes(self):
        with Workdir() as w:
            scenario = write_json(w.path("gather.json"), {"gather": {
                "hold": individual_items(["ca_keo", "ca_keo", "keo_neo"]), "random_fish": False, "monsters": []}})
            inputs = write_json(w.path("inputs.json"), frames({"tick": 0, "interact": True}))
            inventory, gather, quan = w.path("inventory.json"), w.path("g.jsonl"), w.path("q.jsonl")
            code, err = run_headless("--mode", "gather", "--seed", "42", "--ticks", "1",
                                     "--scenario", scenario, "--inputs", inputs,
                                     "--out", gather, "--inventory-out", inventory)
            self.assertEqual(code, 0, err)
            delivered = events(read_jsonl(gather), "gather_end")[0]["data"]["inventory"]["items"]
            self.assertEqual([(x["id"], x["kind"]) for x in delivered], [("I1", "ca_keo"), ("I2", "ca_keo"), ("I3", "keo_neo")])
            code, err = run_headless("--mode", "quan", "--seed", "42", "--ticks", "0",
                                     "--inventory", inventory, "--out", quan)
            self.assertEqual(code, 0, err)
            self.assertEqual(snapshots(read_jsonl(quan))[0]["stock"], delivered)

    def test_keo_neo_node_is_accepted(self):
        with Workdir() as w:
            scenario = write_json(w.path("scenario.json"), {"gather": {
                "nodes": [{"id": "N9", "kind": "keo_neo", "pos": [20, 0]}]}})
            code, err = run_headless("--mode", "gather", "--seed", "1", "--ticks", "0",
                                     "--scenario", scenario, "--out", w.path("out.jsonl"))
            self.assertEqual(code, 0, err)


if __name__ == "__main__":
    unittest.main()

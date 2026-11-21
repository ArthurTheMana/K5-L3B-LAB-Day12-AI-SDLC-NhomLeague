
"""Phase 3 - Gather freshness and individual inventory tests."""

import copy
import unittest

from chonoi.contract import load_contract
from chonoi.ids import IdAllocator
from chonoi.inputs import InputPlayer
from chonoi.sim.gather import GatherSim


class GatherFreshnessTests(unittest.TestCase):

    def make_sim(self, **scenario):
        tuning = copy.deepcopy(load_contract()["tuning"])

        # Enable v1.2 behavior locally without changing team contract.
        tuning["freshness"] = {
            "initial": 100,
            "gather_decay_per_s": 0.5,
            "quan_decay_per_s": 0.25,
            "spoiled_below": 30,
        }

        scenario.setdefault("player", {"pos": [20, 0]})
        scenario.setdefault("nodes", [])
        scenario.setdefault("fish", [])
        scenario.setdefault("random_fish", False)

        return GatherSim(tuning, scenario, None, IdAllocator())

    def tick(self, sim, tick=0, **actions):
        inputs = InputPlayer([{"tick": tick, **actions}] if actions else [])
        return sim.step(inputs.advance(tick))

    def test_create_item_has_unique_id_and_initial_freshness(self):
        sim = self.make_sim()

        first = sim._create_item("ca_linh")
        second = sim._create_item("bong_sung")

        self.assertEqual(first, {
            "id": "I1",
            "kind": "ca_linh",
            "fresh": 100,
        })
        self.assertEqual(second["id"], "I2")
        self.assertEqual(second["fresh"], 100)

    def test_gather_creates_individual_items(self):
        sim = self.make_sim(nodes=[
            {"id": "N1", "kind": "bong_sung", "pos": [20, 0]}
        ])

        events = self.tick(sim, interact=True)

        self.assertIn("gather", [name for name, _ in events])
        self.assertEqual(len(sim.hold), sim.t["node_yield"])
        self.assertTrue(all(item["fresh"] == 100 for item in sim.hold))
        self.assertEqual(
            [item["id"] for item in sim.hold],
            [f"I{i}" for i in range(1, len(sim.hold) + 1)]
        )

    def test_existing_ids_are_reserved_and_not_reused(self):
        sim = self.make_sim(hold=[
            {"id": "I7", "kind": "ca_linh", "fresh": 100}
        ])

        sim.hold.clear()

        item = sim._create_item("ca_linh")
        self.assertEqual(item["id"], "I8")

    def test_freshness_decays_per_tick(self):
        sim = self.make_sim(hold=[
            {"id": "I1", "kind": "ca_linh", "fresh": 100}
        ])

        self.tick(sim)

        self.assertAlmostEqual(
            sim.hold[0]["fresh"],
            100 - 0.5 / 60,
            places=5,
        )

    def test_spoiled_event_occurs_only_once(self):
        sim = self.make_sim(hold=[
            {"id": "I1", "kind": "ca_linh", "fresh": 30}
        ])

        first_events = self.tick(sim, 0)

        self.assertIn(
            ("spoiled", {
                "item_id": "I1",
                "kind": "ca_linh",
                "location": "hold",
            }),
            first_events,
        )
        self.assertLess(sim.hold[0]["fresh"], 30)

        second_events = self.tick(sim, 1)
        self.assertFalse(
            any(name == "spoiled" for name, _ in second_events)
        )

    def test_snapshot_is_independent_of_future_decay(self):
        sim = self.make_sim(hold=[
            {"id": "I1", "kind": "ca_linh", "fresh": 100}
        ])

        old_snapshot = sim.snapshot()
        self.tick(sim)

        self.assertEqual(old_snapshot["hold"][0]["fresh"], 100)
        self.assertLess(sim.snapshot()["hold"][0]["fresh"], 100)

    def test_gather_end_contains_individual_inventory(self):
        sim = self.make_sim(
            player={"pos": [2, 0]},
            hold=[{"id": "I1", "kind": "ca_linh", "fresh": 100}],
        )

        events = self.tick(sim, interact=True)

        end_events = [
            data for name, data in events if name == "gather_end"
        ]

        self.assertEqual(len(end_events), 1)
        self.assertEqual(end_events[0]["reason"], "docked")
        self.assertEqual(
            end_events[0]["inventory"]["items"],
            sim.inventory_items(),
        )
        self.assertIsInstance(
            end_events[0]["inventory"]["items"], list
        )


    def test_multiple_spoiled_events_are_sorted_by_id(self):
        sim = self.make_sim(hold=[
            {"id": "I10", "kind": "ca_linh", "fresh": 30},
            {"id": "I2", "kind": "bong_sung", "fresh": 30},
        ])

        events = self.tick(sim)
        spoiled_ids = [
            data["item_id"]
            for name, data in events
            if name == "spoiled"
        ]

        self.assertEqual(spoiled_ids, ["I2", "I10"])

    def test_freshness_never_goes_below_zero(self):
        sim = self.make_sim(hold=[
            {"id": "I1", "kind": "ca_linh", "fresh": 0}
        ])

        self.tick(sim)

        self.assertEqual(sim.hold[0]["fresh"], 0)

    def test_faint_loses_items_in_lifo_order(self):
        sim = self.make_sim(
            player={
                "pos": [20, 1],
                "hp": 1,
                "oxygen_ticks": 0,
                "zero_oxy_ticks": 0,
            },
            hold=[
                {"id": "I1", "kind": "ca_linh", "fresh": 100},
                {"id": "I2", "kind": "bong_sung", "fresh": 100},
            ],
        )

        sim.t["choke_interval_ticks"] = 1
        events = self.tick(sim)

        faint_data = next(
            data for name, data in events if name == "faint"
        )

        self.assertEqual(
            [item["id"] for item in faint_data["lost"]],
            ["I2", "I1"],
        )
        self.assertEqual(sim.hold, [])
        self.assertEqual(sim.inventory_items(), [])


if __name__ == "__main__":
    unittest.main()

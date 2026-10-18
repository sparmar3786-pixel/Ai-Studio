import unittest
from datetime import datetime, timezone
from bot_ai.rules_engine import MarketSnapshot, evaluate


class RulesEngineTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
        self.ts = self.now.isoformat()

    def test_stale_data_fails_closed(self):
        s = MarketSnapshot("NIFTY", "NIFTY", "2020-01-01T00:00:00+00:00", price=100)
        out = evaluate(s, now=self.now)
        self.assertEqual(out["side"], "WAIT")
        self.assertIsNone(out["entry"])
        self.assertFalse(out["order_placement"])

    def test_missing_price_fails_closed(self):
        s = MarketSnapshot("MCX", "GOLD", self.ts)
        self.assertEqual(evaluate(s, now=self.now)["side"], "WAIT")

    def test_no_strategy_signal_waits(self):
        s = MarketSnapshot("NIFTY", "NIFTY", self.ts, price=100)
        self.assertEqual(evaluate(s, now=self.now)["side"], "WAIT")

    def test_conflicting_strategies_wait(self):
        s = MarketSnapshot(
            "NIFTY", "NIFTY", self.ts, price=110,
            opening_range_high=105, opening_range_low=95,
            vwap=120, confirmation=True, stop_loss=100, target=130
        )
        out = evaluate(s, now=self.now)
        self.assertEqual(out["side"], "WAIT")
        self.assertIn("strategy_conflict", out["reasons"])

    def test_valid_candidate_is_not_an_order(self):
        s = MarketSnapshot(
            "NIFTY", "NIFTY", self.ts, price=110,
            opening_range_high=105, opening_range_low=95,
            confirmation=True, stop_loss=100, target=130
        )
        out = evaluate(s, now=self.now)
        self.assertEqual(out["status"], "CANDIDATE")
        self.assertEqual(out["side"], "BUY")
        self.assertFalse(out["order_placement"])


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

from netwatch import database


class DatabaseTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"

        self.path_patcher = patch.object(
            database,
            "DB_PATH",
            self.db_path,
        )
        self.path_patcher.start()

        database.init_database()

    def tearDown(self):
        self.path_patcher.stop()
        self.temp_dir.cleanup()

    def test_save_measurement(self):
        result = SimpleNamespace(
            host="127.0.0.1",
            reachable=True,
            latency_ms=2.5,
            packet_loss=0,
            timestamp=1000.0,
        )

        database.save_measurement(result)

        summary = database.get_host_summary("127.0.0.1")

        self.assertEqual(summary["total_checks"], 1)
        self.assertEqual(summary["failures"], 0)
        self.assertEqual(summary["avg_latency"], 2.5)

    def test_packet_loss_calculation_data(self):
        online = SimpleNamespace(
            host="1.1.1.1",
            reachable=True,
            latency_ms=5.0,
            packet_loss=0,
            timestamp=1000.0,
        )

        offline = SimpleNamespace(
            host="1.1.1.1",
            reachable=False,
            latency_ms=None,
            packet_loss=100,
            timestamp=1001.0,
        )

        database.save_measurement(online)
        database.save_measurement(offline)

        summary = database.get_host_summary("1.1.1.1")

        self.assertEqual(summary["total_checks"], 2)
        self.assertEqual(summary["failures"], 1)

    def test_empty_host(self):
        summary = database.get_host_summary("unknown")

        self.assertEqual(summary["total_checks"], 0)
        self.assertEqual(summary["failures"], 0)


if __name__ == "__main__":
    unittest.main()

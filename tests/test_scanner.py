import unittest
from unittest.mock import patch

from netwatch.scanner import scan_ports, scan_port
from netwatch.reporter import generate_report


class ScannerTests(unittest.TestCase):

    def test_invalid_port(self):
        with self.assertRaises(ValueError):
            scan_ports("127.0.0.1", [70000])

    def test_empty_ports(self):
        with self.assertRaises(ValueError):
            scan_ports("127.0.0.1", [])

    @patch("netwatch.scanner.socket.create_connection")
    def test_open_port(self, mock_connection):
        mock_connection.return_value.__enter__.return_value = None

        result = scan_port("127.0.0.1", 80)

        self.assertTrue(result.open)
        self.assertEqual(result.port, 80)

    @patch("netwatch.scanner.socket.create_connection")
    def test_closed_port(self, mock_connection):
        mock_connection.side_effect = OSError()

        result = scan_port("127.0.0.1", 65000)

        self.assertFalse(result.open)


class ReporterTests(unittest.TestCase):

    def test_report_generation(self):
        summary = {
            "total_checks": 10,
            "failures": 2,
            "min_latency": 1.0,
            "max_latency": 10.0,
            "avg_latency": 5.0,
        }

        report = generate_report("127.0.0.1", summary)

        self.assertIn("127.0.0.1", report)
        self.assertIn("80.00%", report)
        self.assertIn("Average latency", report)


if __name__ == "__main__":
    unittest.main()

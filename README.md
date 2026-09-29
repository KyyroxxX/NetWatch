# NetWatch

**Concurrent Network Monitoring & Historical Analysis Tool**

NetWatch is a lightweight Python network monitoring tool designed to
monitor multiple hosts concurrently, detect availability changes,
calculate latency statistics, and persist measurements using SQLite.

## Features

- Concurrent host monitoring using ThreadPoolExecutor.
- Host availability detection.
- Latency statistics: minimum, maximum, and average.
- Packet loss calculation.
- Detection of host outages and recoveries.
- Persistent measurement storage with SQLite.
- Historical measurement viewer.
- Logging of monitoring events.
- Graceful shutdown with Ctrl+C.
- Unit tests using Python's unittest framework.
- No third-party dependencies.

## Architecture

```text
NetWatch/
├── main.py
├── history.py
├── netwatch/
│   ├── __init__.py
│   ├── monitor.py
│   ├── database.py
│   ├── alerts.py
│   ├── reporter.py
│   └── scanner.py
├── tests/
│   └── test_database.py
├── config/
├── data/
├── docs/
├── logs/
├── requirements.txt
└── README.md


Requirements
- Python 3.10+
- System ping utility
- Linux, macOS, or Windows
Installation
Clone the repository:
git clone https://github.com/KyyroxxX/NetWatch.git
cd NetWatch


Create a virtual environment:
python -m venv .venv


Activate it on Linux:
source .venv/bin/activate


No external Python packages are required.
Usage
Monitor multiple hosts:
python main.py 127.0.0.1 1.1.1.1 8.8.8.8


Configure the monitoring interval:
python main.py 1.1.1.1 8.8.8.8 --interval 3


Configure the ping timeout:
python main.py 1.1.1.1 --timeout 5 --interval 2


Stop monitoring with Ctrl+C.
Historical Data
View the latest measurements:
python history.py


Specify the number of records:
python history.py --limit 50


Measurements are stored locally in:
data/netwatch.db


Testing
Run the unit tests:
python -m unittest discover -s tests -v


Check Python syntax:
python -m compileall -q main.py history.py netwatch tests


Technical Notes
NetWatch uses Python's standard library:
- subprocess for system ping execution.
- concurrent.futures for concurrent monitoring.
- sqlite3 for persistent storage.
- logging for event logging.
- argparse for command-line arguments.
- unittest for automated tests.
Latency currently represents the elapsed execution time of the system
ping command, rather than an ICMP round-trip time parsed directly from
the ping response.
Packet loss is calculated from recorded monitoring results.
Limitations
- Monitoring requires the system ping utility.
- Some hosts or networks may block ICMP traffic.
- Historical measurements are stored locally.
- No graphical dashboard or remote alerting is currently included.
Author
Alejandro De Luque
GitHub: @KyyroxxX
License
MIT License.


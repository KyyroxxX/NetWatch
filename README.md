# NetWatch

**Concurrent Network Monitoring & Historical Analysis Tool**

[English](#english) · [Español](#español)

---

## English

NetWatch is a lightweight Python network monitoring tool designed to monitor multiple hosts concurrently, detect availability changes, calculate latency statistics, and persist measurements using SQLite.

### Features

- Concurrent host monitoring using `ThreadPoolExecutor`.
- Host availability detection.
- Latency statistics: minimum, maximum, and average.
- Packet loss calculation.
- Detection of host outages and recoveries.
- Persistent measurement storage with SQLite.
- Historical measurement viewer.
- Logging of monitoring events.
- Graceful shutdown with Ctrl+C.
- Unit tests using Python's `unittest` framework.
- No third-party dependencies.

### Architecture

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
```

### Requirements

- Python 3.10+
- System `ping` utility
- Linux, macOS, or Windows

### Installation

Clone the repository:

```bash
git clone https://github.com/KyyroxxX/NetWatch.git
cd NetWatch
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

No external Python packages are required.

### Usage

Monitor multiple hosts:

```bash
python main.py 127.0.0.1 1.1.1.1 8.8.8.8
```

Configure the monitoring interval:

```bash
python main.py 1.1.1.1 8.8.8.8 --interval 3
```

Configure the ping timeout:

```bash
python main.py 1.1.1.1 --timeout 5 --interval 2
```

Stop monitoring with Ctrl+C.

### Historical Data

View the latest measurements:

```bash
python history.py
```

Specify the number of records:

```bash
python history.py --limit 50
```

Measurements are stored locally in:

```text
data/netwatch.db
```

### Testing

Run the unit tests:

```bash
python -m unittest discover -s tests -v
```

Check Python syntax:

```bash
python -m compileall -q main.py history.py netwatch tests
```

### Technical Notes

NetWatch uses Python's standard library:

- `subprocess` for system ping execution.
- `concurrent.futures` for concurrent monitoring.
- `sqlite3` for persistent storage.
- `logging` for event logging.
- `argparse` for command-line arguments.
- `unittest` for automated tests.

Latency currently represents the elapsed execution time of the system `ping` command, rather than an ICMP round-trip time parsed directly from the ping response.

Packet loss is calculated from recorded monitoring results.

### Limitations

- Monitoring requires the system `ping` utility.
- Some hosts or networks may block ICMP traffic.
- Historical measurements are stored locally.
- No graphical dashboard or remote alerting is currently included.

### Author

Alejandro De Luque  
GitHub: [@KyyroxxX](https://github.com/KyyroxxX)

### License

MIT License.

---

## Español

NetWatch es una herramienta ligera de monitorización de redes desarrollada en Python. Permite supervisar varios hosts de forma concurrente, detectar cambios de disponibilidad, calcular estadísticas de latencia y guardar mediciones en una base de datos SQLite.

### Funcionalidades

- Monitorización concurrente de hosts mediante `ThreadPoolExecutor`.
- Detección de disponibilidad de los hosts.
- Estadísticas de latencia: mínima, máxima y media.
- Cálculo de pérdida de paquetes.
- Detección de caídas y recuperaciones de hosts.
- Almacenamiento persistente de mediciones con SQLite.
- Consulta del histórico de mediciones.
- Registro de eventos de monitorización.
- Cierre controlado mediante Ctrl+C.
- Pruebas unitarias con el framework `unittest` de Python.
- Sin dependencias externas de Python.

### Arquitectura

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
```

### Requisitos

- Python 3.10 o superior.
- Utilidad del sistema `ping`.
- Linux, macOS o Windows.

### Instalación

Clona el repositorio:

```bash
git clone https://github.com/KyyroxxX/NetWatch.git
cd NetWatch
```

Crea un entorno virtual:

```bash
python -m venv .venv
```

Actívalo en Linux:

```bash
source .venv/bin/activate
```

No se necesitan paquetes externos de Python.

### Uso

Monitorizar varios hosts:

```bash
python main.py 127.0.0.1 1.1.1.1 8.8.8.8
```

Configurar el intervalo de monitorización:

```bash
python main.py 1.1.1.1 8.8.8.8 --interval 3
```

Configurar el tiempo de espera de ping:

```bash
python main.py 1.1.1.1 --timeout 5 --interval 2
```

Para detener la monitorización, pulsa Ctrl+C.

### Datos históricos

Consultar las últimas mediciones:

```bash
python history.py
```

Indicar el número de registros:

```bash
python history.py --limit 50
```

Las mediciones se almacenan localmente en:

```text
data/netwatch.db
```

### Pruebas

Ejecutar las pruebas unitarias:

```bash
python -m unittest discover -s tests -v
```

Comprobar la sintaxis de Python:

```bash
python -m compileall -q main.py history.py netwatch tests
```

### Notas técnicas

NetWatch utiliza la biblioteca estándar de Python:

- `subprocess` para ejecutar el comando ping del sistema.
- `concurrent.futures` para la monitorización concurrente.
- `sqlite3` para el almacenamiento persistente.
- `logging` para registrar eventos.
- `argparse` para gestionar los argumentos de línea de comandos.
- `unittest` para las pruebas automatizadas.

La latencia representa actualmente el tiempo transcurrido durante la ejecución del comando `ping` del sistema, y no un tiempo de ida y vuelta ICMP extraído directamente de la respuesta de ping.

La pérdida de paquetes se calcula a partir de los resultados de monitorización registrados.

### Limitaciones

- La monitorización requiere la utilidad `ping` del sistema.
- Algunos hosts o redes pueden bloquear el tráfico ICMP.
- Las mediciones históricas se almacenan localmente.
- Actualmente no incluye un panel gráfico ni alertas remotas.

### Autor

Alejandro De Luque  
GitHub: [@KyyroxxX](https://github.com/KyyroxxX)

### Licencia

Licencia MIT.

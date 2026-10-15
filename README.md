# Python Based Satellite Modem Test Automation Framework

## Overview

This project is a Python-based satellite modem test automation framework developed to simulate and automate the verification of key communication system performance parameters.

The framework demonstrates how software can be used to automate RF and communication system validation by comparing measured modem performance against predefined engineering requirements stored in a YAML configuration file.

The project was developed to strengthen practical skills in Python automation, verification workflows, logging, reporting.

---

## Features

✔ YAML-based test configuration

✔ Automated verification of

* Signal-to-Noise Ratio (SNR)
* Bit Error Rate (BER)
* Network Latency
* Throughput

✔ Automatic PASS / FAIL evaluation

✔ Randomized modem simulator for realistic testing

✔ Timestamped execution history

✔ CSV result logging

✔ Automatic PDF verification report generation

✔ Logging of every execution

✔ Modular project structure

✔ Git version control

---

## Project Structure

```
satcom_test_automation/
│
├── configs/
│   └── test_requirements.yaml
│
├── src/
│   └── modem_simulator.py
│
├── results/
│   ├── test_results.csv
│   └── Verification Reports
│
├── logs/
│   └── test_run.log
│
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Technologies Used

* Python 3.12
* PyYAML
* CSV
* Logging
* ReportLab
* Git
* GitHub

---

## Test Parameters

| Test | Requirement |
|-------|------------|
| SNR | ≥ 10 dB |
| BER | ≤ 1 × 10⁻⁶ |
| Latency | ≤ 50 ms |
| Throughput | ≥ 20 Mbps |

---

## How It Works

1. Load test requirements from the YAML configuration.
2. Simulate satellite modem measurements.
3. Compare measured values against configured limits.
4. Evaluate each test as PASS or FAIL.
5. Store execution history in a CSV file.
6. Generate a timestamped PDF verification report.
7. Record execution details in the application log.

---

## Sample CSV Output
| Run ID | Date | Time | Overall Status | SNR (dB) | BER | Latency (ms) | Throughput (Mbps) | SNR Status | BER Status | Latency Status | Throughput Status |
|--------|------|------|---------------|---------:|------------:|-------------:|------------------:|------------|------------|----------------|-------------------|
| 20260703_101523 | 2026-07-03 | 10:15:23 | PASS | 14.82 | 5.0e-07 | 32.45 | 31.78 | PASS | PASS | PASS | PASS |
| 20260703_101847 | 2026-07-03 | 10:18:47 | FAIL | 9.41 | 1.0e-07 | 56.23 | 24.35 | FAIL | PASS | FAIL | PASS |
| 20260703_102214 | 2026-07-03 | 10:22:14 | FAIL | 11.54 | 2.0e-06 | 61.02 | 18.94 | PASS | FAIL | FAIL | FAIL |
| 20260703_102603 | 2026-07-03 | 10:26:03 | PASS | 15.37 | 1.0e-07 | 29.86 | 34.52 | PASS | PASS | PASS | PASS |
---

## Example Console Output

```
Satellite Modem Test Results

Run ID: 20260703_102301

SNR Test .............. PASS
BER Test .............. PASS
Latency Test .......... PASS
Throughput Test ....... PASS

Overall Status ........ PASS

CSV log updated successfully.
Verification report generated successfully.
```

---

## Running the Project

Clone the repository

```bash
git clone https://github.com/aryanjadhav/satcom_test_automation.git
```

Navigate to the project

```bash
cd satcom_test_automation
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python main.py
```

---

## Learning Outcomes

This project demonstrates practical experience in

* Python Programming
* Automation
* Communication Systems
* Verification & Validation
* YAML Configuration Management
* Logging and Reporting
* Git and GitHub Workflow

---

## Author

**Aryan Jadhav**

Master's Student

Electrical Engineering & Information Technology

Communication Systems

Python | RF Testing | Test Automation | Satellite Communications

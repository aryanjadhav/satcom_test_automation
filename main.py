import os
import csv
import yaml
import logging
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.modem_simulator import SatelliteModemSimulator

RESULTS_DIR = "results"
LOGS_DIR = "logs"

CSV_FILE = os.path.join(RESULTS_DIR, "test_results.csv")
LOG_FILE = os.path.join(LOGS_DIR, "test_run.log")

def setup_project_files():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def get_run_metadata():
    now = datetime.now()

    return {
        "run_id": now.strftime("%Y%m%d_%H%M%S"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timestamp": now.isoformat(timespec="seconds")
    } 


def load_requirements():
    with open("configs/test_requirements.yaml", "r") as file:
        return yaml.safe_load(file)

def run_tests():
    requirements = load_requirements()
    modem = SatelliteModemSimulator()

    results = {}

    snr = modem.measure_snr()
    results["SNR Test"] = {
        "measured": snr,
        "limit": requirements["tests"]["snr_test"]["minimum_snr_db"],
        "unit": "dB",
        "requirement": "minimum_snr_db",
        "status": "PASS" if snr >= requirements["tests"]["snr_test"]["minimum_snr_db"] else "FAIL"
    }

    ber = modem.measure_ber()
    results["BER Test"] = {
        "measured": ber,
        "limit": requirements["tests"]["ber_test"]["maximum_ber"],
        "unit": "ratio",
        "requirement": "maximum_ber",
        "status": "PASS" if ber <= requirements["tests"]["ber_test"]["maximum_ber"] else "FAIL"
    }

    latency = modem.measure_latency()
    results["Latency Test"] = {
        "measured": latency,
        "limit": requirements["tests"]["latency_test"]["maximum_latency_ms"],
        "unit": "ms",
        "requirement": "maximum_latency_ms",
        "status": "PASS" if latency <= requirements["tests"]["latency_test"]["maximum_latency_ms"] else "FAIL"
    }

    throughput = modem.measure_throughput()
    results["Throughput Test"] = {
        "measured": throughput,
        "limit": requirements["tests"]["throughput_test"]["minimum_throughput_mbps"],
        "unit": "Mbps",
        "requirement": "minimum_throughput_mbps",
        "status": "PASS" if throughput >= requirements["tests"]["throughput_test"]["minimum_throughput_mbps"] else "FAIL"
    }

    return results

def append_results_to_csv(results, run_info):

    file_exists = os.path.exists(CSV_FILE)

    overall_status = (
        "PASS"
        if all(result["status"] == "PASS" for result in results.values())
        else "FAIL"
    )

    with open(CSV_FILE, "a", newline="") as csv_file:

        fieldnames = [
            "Run ID",
            "Date",
            "Time",
            "Overall Status",

            "SNR (dB)",
            "BER",
            "Latency (ms)",
            "Throughput (Mbps)",

            "SNR Status",
            "BER Status",
            "Latency Status",
            "Throughput Status"
        ]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "Run ID": run_info["run_id"],
            "Date": run_info["date"],
            "Time": run_info["time"],
            "Overall Status": overall_status,

            "SNR (dB)": results["SNR Test"]["measured"],
            "BER": results["BER Test"]["measured"],
            "Latency (ms)": results["Latency Test"]["measured"],
            "Throughput (Mbps)": results["Throughput Test"]["measured"],

            "SNR Status": results["SNR Test"]["status"],
            "BER Status": results["BER Test"]["status"],
            "Latency Status": results["Latency Test"]["status"],
            "Throughput Status": results["Throughput Test"]["status"]
        })

def write_log(results, run_info):
    logging.info("New satellite modem test run started")
    logging.info(f"Run ID: {run_info['run_id']}")
    logging.info(f"Timestamp: {run_info['timestamp']}")

    for test_name, result in results.items():
        logging.info(
            f"{test_name} | "
            f"Measured: {result['measured']} {result['unit']} | "
            f"Limit: {result['limit']} {result['unit']} | "
            f"Status: {result['status']}"
        )

    logging.info("Test run completed")

def generate_pdf_report(results, run_info):
    overall_status = "PASS" if all(
        result["status"] == "PASS" for result in results.values()
    ) else "FAIL"

    pdf_file = os.path.join(
        RESULTS_DIR,
        f"{run_info['run_id']}_SatelliteModem_VerificationReport_{overall_status}.pdf"
    )

    pdf = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4

    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Satellite Modem Test Automation Verification Report")

    y -= 40

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Run ID: {run_info['run_id']}")
    y -= 18
    pdf.drawString(50, y, f"Date: {run_info['date']}")
    y -= 18
    pdf.drawString(50, y, f"Time: {run_info['time']}")
    y -= 18
    pdf.drawString(50, y, f"Timestamp: {run_info['timestamp']}")

    y -= 35

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Test Name")
    pdf.drawString(180, y, "Measured")
    pdf.drawString(280, y, "Limit")
    pdf.drawString(380, y, "Unit")
    pdf.drawString(450, y, "Status")

    y -= 15
    pdf.line(50, y, 540, y)
    y -= 20

    pdf.setFont("Helvetica", 10)

    for test_name, result in results.items():
        pdf.drawString(50, y, test_name)
        pdf.drawString(180, y, str(result["measured"]))
        pdf.drawString(280, y, str(result["limit"]))
        pdf.drawString(380, y, result.get("unit", ""))
        pdf.drawString(450, y, result["status"])
        y -= 22

    y -= 25

    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result["status"] == "PASS")
    failed_tests = total_tests - passed_tests

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Summary")

    y -= 20

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Total Tests: {total_tests}")
    y -= 18
    pdf.drawString(50, y, f"Passed Tests: {passed_tests}")
    y -= 18
    pdf.drawString(50, y, f"Failed Tests: {failed_tests}")

    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, f"Final Verification Status: {overall_status}")

    pdf.save()

    return pdf_file


if __name__ == "__main__":
    setup_project_files()

    run_info = get_run_metadata()
    test_results = run_tests()

    append_results_to_csv(test_results, run_info)
    write_log(test_results, run_info)
    pdf_file = generate_pdf_report(test_results, run_info)

    print("Satellite Modem Test Results")
    print(f"Run ID: {run_info['run_id']}")
    print(f"Timestamp: {run_info['timestamp']}")
    print()

    for test_name, result in test_results.items():
        print(test_name, result)

    print()
    print(f"Results appended to: {CSV_FILE}")
    print(f"Log saved to: {LOG_FILE}")
    print(f"PDF report saved to: {pdf_file}")
import random


class SatelliteModemSimulator:
    def __init__(self):
        self.overall_case = random.choice(["PASS_CASE", "FAIL_CASE"])

        self.test_outcomes = {
            "snr": True,
            "ber": True,
            "latency": True,
            "throughput": True
        }

        if self.overall_case == "FAIL_CASE":
            number_of_failed_tests = random.choice([1, 2, 3, 4])
            failed_tests = random.sample(
                list(self.test_outcomes.keys()),
                number_of_failed_tests
            )

            for test in failed_tests:
                self.test_outcomes[test] = False

    def measure_snr(self):
        if self.test_outcomes["snr"]:
            return round(random.uniform(10, 18), 2)
        return round(random.uniform(8, 9.99), 2)

    def measure_ber(self):
        if self.test_outcomes["ber"]:
            return random.choice([1e-7, 5e-7, 8e-7])
        return random.choice([2e-6, 5e-6, 1e-5])

    def measure_latency(self):
        if self.test_outcomes["latency"]:
            return round(random.uniform(20, 50), 2)
        return round(random.uniform(50.01, 80), 2)

    def measure_throughput(self):
        if self.test_outcomes["throughput"]:
            return round(random.uniform(20, 40), 2)
        return round(random.uniform(10, 19.99), 2)
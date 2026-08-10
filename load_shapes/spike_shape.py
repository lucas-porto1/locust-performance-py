from locust import LoadTestShape


class SpikeTestShape(LoadTestShape):
    stages = (
        {"duration": 30, "users": 5, "spawn_rate": 1},
        {"duration": 60, "users": 40, "spawn_rate": 40},
        {"duration": 120, "users": 40, "spawn_rate": 1},
        {"duration": 150, "users": 5, "spawn_rate": 35},
    )

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None

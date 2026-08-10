from locust import LoadTestShape


class StressTestShape(LoadTestShape):
    stages = (
        {"duration": 60, "users": 10, "spawn_rate": 2},
        {"duration": 120, "users": 20, "spawn_rate": 2},
        {"duration": 180, "users": 30, "spawn_rate": 3},
        {"duration": 240, "users": 40, "spawn_rate": 3},
        {"duration": 300, "users": 50, "spawn_rate": 5},
    )

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None

class Metrics:
    def __init__(self):
        self.total = 0
        self.accepted = 0
        self.rejected = 0
        self.scores = []

    def log_accept(self, score: float):
        self.total += 1
        self.accepted += 1
        self.scores.append(score)

    def log_reject(self):
        self.total += 1
        self.rejected += 1

    def summary(self):
        if self.scores:
            avg_score = sum(self.scores) / len(self.scores)
        else:
            avg_score = 0.0

        return {
            "total_exercises": self.total,
            "accepted": self.accepted,
            "rejected": self.rejected,
            "acceptance_rate": self.accepted / max(1, self.total),
            "average_score": avg_score
        }

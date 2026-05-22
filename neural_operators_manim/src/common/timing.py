from manim import MovingCameraScene


class TimedScene(MovingCameraScene):
    """Scene with script-time aligned animation helpers."""

    def setup(self):
        super().setup()
        self.t = 0.0

    def play_timed(self, label: str, start: float, end: float, *animations, **kwargs):
        if start < self.t - 1e-6:
            raise ValueError(f"{label}: start={start} before current time={self.t}")
        if start > self.t:
            self.wait(start - self.t)
        duration = end - start
        if duration <= 0:
            raise ValueError(f"{label}: non-positive duration")
        self.play(*animations, run_time=duration, **kwargs)
        self.t = end

    def wait_timed(self, label: str, start: float, end: float):
        if start < self.t - 1e-6:
            raise ValueError(f"{label}: start={start} before current time={self.t}")
        if start > self.t:
            self.wait(start - self.t)
        duration = end - start
        if duration > 0:
            self.wait(duration)
        self.t = end

    def pad_to(self, target_time: float):
        if target_time < self.t - 1e-6:
            raise ValueError(f"Scene exceeded target={target_time}; current={self.t}")
        if target_time > self.t:
            self.wait(target_time - self.t)
        self.t = target_time


def global_to_local(global_time: float, scene_start: float) -> float:
    return global_time - scene_start


def parse_timecode(timecode: str) -> float:
    parts = timecode.split(":")
    if len(parts) == 2:
        minutes, seconds = parts
        return float(minutes) * 60 + float(seconds)
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    return float(timecode)


import unittest
from datetime import datetime, timedelta

from tracker import Tracker


class FakeDetection:
    def __init__(self, bbox, confidence=0.9):
        self.bbox = bbox
        self.confidence = confidence


class TrackerJitterTest(unittest.TestCase):
    def test_bbox_center_uses_average_of_most_recent_five_frames(self):
        tracker = Tracker()
        now = datetime(2026, 9, 26, 12, 0, 0)

        for center_x in (5, 7, 9, 11, 13, 15):
            tracker.tracking(
                [FakeDetection((center_x - 5, 0, center_x + 5, 10))],
                now,
            )
            now += timedelta(milliseconds=100)

        target = tracker.target_list[0]

        self.assertEqual(target.target_id, 1)
        self.assertEqual(len(target.center_history), 5)
        self.assertEqual(target.bbox, (6, 0, 16, 10))


if __name__ == "__main__":
    unittest.main()

"""Business decision test; it does not call the gateway."""

import unittest

from field_followup import WorkOrder, follow_up_for


class FollowUpDecisionTest(unittest.TestCase):
    def test_assigned_order_with_photo_note_gets_arrival_confirmation(self) -> None:
        order = WorkOrder("WO-1042", "Moisture near lower seal", "assigned")
        self.assertEqual(follow_up_for(order), "confirm_arrival_window")


if __name__ == "__main__":
    unittest.main()


from datetime import datetime


class Activity:
    """
    Activity Model
    Stores user activities performed in the system.
    """

    def __init__(
        self,
        id=None,
        user_id=None,
        task_id=None,
        action="",
        activity_time=None
    ):
        self.id = id
        self.user_id = user_id
        self.task_id = task_id
        self.action = action
        self.activity_time = activity_time or datetime.now()

    # -----------------------------------------
    # Update Activity
    # -----------------------------------------

    def update_action(self, action):
        self.action = action
        self.activity_time = datetime.now()

    # -----------------------------------------
    # Convert Object to Dictionary
    # -----------------------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "action": self.action,
            "activity_time": self.activity_time
        }

    # -----------------------------------------
    # String Representation
    # -----------------------------------------

    def __str__(self):
        return (
            f"Activity("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"task_id={self.task_id}, "
            f"action='{self.action}', "
            f"time='{self.activity_time}')"
        )
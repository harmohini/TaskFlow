from datetime import datetime


class Workflow:
    """
    Workflow Model
    Handles workflow transitions for tasks.
    """

    # Valid workflow stages
    STAGES = [
        "To Do",
        "In Progress",
        "Review",
        "Completed"
    ]

    # Allowed transitions
    VALID_TRANSITIONS = {
        "To Do": ["In Progress"],
        "In Progress": ["Review"],
        "Review": ["Completed", "In Progress"],
        "Completed": []
    }

    def __init__(
        self,
        id=None,
        task_id=None,
        current_stage="To Do",
        previous_stage=None,
        updated_by=None,
        updated_at=None
    ):
        self.id = id
        self.task_id = task_id
        self.current_stage = current_stage
        self.previous_stage = previous_stage
        self.updated_by = updated_by
        self.updated_at = updated_at or datetime.now()

    # ----------------------------------------
    # Check if transition is valid
    # ----------------------------------------

    def can_move_to(self, new_stage):
        return new_stage in self.VALID_TRANSITIONS.get(
            self.current_stage,
            []
        )

    # ----------------------------------------
    # Move Workflow
    # ----------------------------------------

    def move_to(self, new_stage, user_id):

        if not self.can_move_to(new_stage):
            raise ValueError(
                f"Cannot move from '{self.current_stage}' to '{new_stage}'"
            )

        self.previous_stage = self.current_stage
        self.current_stage = new_stage
        self.updated_by = user_id
        self.updated_at = datetime.now()

    # ----------------------------------------
    # Restart Workflow
    # ----------------------------------------

    def restart(self):

        self.previous_stage = self.current_stage
        self.current_stage = "To Do"
        self.updated_at = datetime.now()

    # ----------------------------------------
    # Is Completed?
    # ----------------------------------------

    def is_completed(self):
        return self.current_stage == "Completed"

    # ----------------------------------------
    # Convert to Dictionary
    # ----------------------------------------

    def to_dict(self):

        return {
            "id": self.id,
            "task_id": self.task_id,
            "previous_stage": self.previous_stage,
            "current_stage": self.current_stage,
            "updated_by": self.updated_by,
            "updated_at": self.updated_at
        }

    # ----------------------------------------
    # String Representation
    # ----------------------------------------

    def __str__(self):

        return (
            f"Workflow("
            f"task_id={self.task_id}, "
            f"current_stage='{self.current_stage}')"
        )
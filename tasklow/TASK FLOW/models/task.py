from datetime import date, datetime


class Task:
    """
    Task Model
    Represents a task within a project in TaskFlow.
    """

    def __init__(
        self,
        id=None,
        project_id=None,
        assigned_to=None,
        title="",
        description="",
        priority="Medium",
        status="To Do",
        due_date=None,
        created_at=None,
        updated_at=None
    ):
        self.id = id
        self.project_id = project_id
        self.assigned_to = assigned_to
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    # ------------------------------------
    # Valid Priorities
    # ------------------------------------

    @staticmethod
    def valid_priorities():
        return ["Low", "Medium", "High", "Critical"]

    # ------------------------------------
    # Valid Statuses
    # ------------------------------------

    @staticmethod
    def valid_statuses():
        return ["To Do", "In Progress", "Review", "Completed"]

    # ------------------------------------
    # Update Task Fields
    # ------------------------------------

    def update_task(
        self,
        title=None,
        description=None,
        priority=None,
        status=None,
        due_date=None,
        assigned_to=None
    ):
        if title:
            self.title = title
        if description is not None:
            self.description = description
        if priority and priority in self.valid_priorities():
            self.priority = priority
        if status and status in self.valid_statuses():
            self.status = status
        if due_date:
            self.due_date = due_date
        if assigned_to is not None:
            self.assigned_to = assigned_to
        self.updated_at = datetime.now()

    # ------------------------------------
    # Change Status
    # ------------------------------------

    def change_status(self, new_status):
        if new_status in self.valid_statuses():
            self.status = new_status
            self.updated_at = datetime.now()
        else:
            raise ValueError(f"Invalid task status: {new_status}")

    # ------------------------------------
    # Convert Object to Dictionary
    # ------------------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "assigned_to": self.assigned_to,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    # ------------------------------------
    # String Representation
    # ------------------------------------

    def __str__(self):
        return (
            f"Task("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"status='{self.status}', "
            f"priority='{self.priority}')"
        )
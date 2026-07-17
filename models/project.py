from datetime import date


class Project:
    """
    Project Model
    Represents a project in TaskFlow.
    """

    def __init__(
        self,
        id=None,
        project_name="",
        description="",
        start_date=None,
        end_date=None,
        status="Active",
        created_by=None,
        created_at=None
    ):
        self.id = id
        self.project_name = project_name
        self.description = description
        self.start_date = start_date or date.today()
        self.end_date = end_date
        self.status = status
        self.created_by = created_by
        self.created_at = created_at

    # ------------------------------------
    # Update Project Information
    # ------------------------------------

    def update_project(
        self,
        project_name=None,
        description=None,
        start_date=None,
        end_date=None,
        status=None
    ):
        if project_name:
            self.project_name = project_name

        if description:
            self.description = description

        if start_date:
            self.start_date = start_date

        if end_date:
            self.end_date = end_date

        if status:
            self.status = status

    # ------------------------------------
    # Change Status
    # ------------------------------------

    def change_status(self, status):
        allowed_status = [
            "Active",
            "Completed",
            "On Hold",
            "Cancelled"
        ]

        if status in allowed_status:
            self.status = status
        else:
            raise ValueError("Invalid Project Status")

    # ------------------------------------
    # Convert Object to Dictionary
    # ------------------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "project_name": self.project_name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "created_by": self.created_by,
            "created_at": self.created_at
        }

    # ------------------------------------
    # String Representation
    # ------------------------------------

    def __str__(self):
        return (
            f"Project("
            f"id={self.id}, "
            f"name='{self.project_name}', "
            f"status='{self.status}')"
        )
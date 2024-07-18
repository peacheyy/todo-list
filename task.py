class Task:
    def __init__(self, title, description, due_date=None, complete=False, priority='medium'):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.complete = complete
        self.priority = priority  # Add priority attribute

    def mark_as_complete(self):
        self.complete = True

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "complete": self.complete,
            "priority": self.priority  # Include priority in the dictionary
        }

    def __str__(self):
        status = "Complete" if self.complete else "Incomplete"
        return (f"Task: {self.title}\n"
                f"Description: {self.description}\n"
                f"Due Date: {self.due_date}\n"
                f"Priority: {self.priority}\n"
                f"Status: {status}")

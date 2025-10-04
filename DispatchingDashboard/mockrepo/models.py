# The different Tables within the ERD

#Resource -> is basically the Engineer
# SkillGroup -> Basically the lines/points

from datetime import datetime
import uuid
import random

# --- Skill Group Table --- #
class SkillGroup:
    """ Mirrors the SkillGroup ERD table. """
    def __init__(self, skillGroupID: str, name: str, points: int):
        self.skillGroupID = skillGroupID
        self.name = name 
        self.points = points
    
    def to_dict(self):
        return {"id": self.skillGroupID, "name": self.name, "points": self.points}
    

# Engineers known as Resource
class Resource:
    """ Mirrors the Resource ERD tablee (the engineer). """
    def __init__(self, resourceID: str, name: str):
        self.resourceID = resourceID
        self.name = name

    def to_dict(self):
        return {"id": self.resourceID, "name": self.name}
    
# Tickets currently in the queue
class VirtualQueueTicket:
    """ Mirrors the VirtualQueueTicket ERD table. """
    def __init__(self, skillGroupID: str, priority: int, expected_minutes: int):
        self.ticketID = str(uuid.uuid4())[:8]
        self.skillGroupID = skillGroupID
        self.priority = priority
        self.expected_minutes = expected_minutes
        self.weighted_importance = random.uniform(0.5, 1.5) # Set Weighted importance to random since I do not have the logic
        self.created_date = datetime.now()
        self.updated_date = datetime.now()
    
    def to_dict(self):
        # Format dates for cleaner JSON
        return {k: v.isoformat() if isinstance(v, datetime) else v for k, v in self.__dict__.items()}
    
class ArchivedTicket(VirtualQueueTicket): # Most likely need to update I believe I need the SkillGroup info
    """ Extends VirtualQueueTicket with completion fields. """
    def __init__(self, ticket: VirtualQueueTicket, skillGroupID: str, resourceID: str, points_awarded: int):
        super().__init__(ticket.skillGroupID, ticket.priority, ticket.expected_minutes)
        self.ticketID = ticket.ticketID
        self.skillGroupID = skillGroupID
        self.resourceID = resourceID
        self.actual_minutes = random.randint(10, ticket.expected_minutes + 15)
        self.status = "Completed"
        self.is_completed = True
        self.completed_date = datetime.now()
        self.points_awarded = points_awarded

    def to_dict(self):
        # Include base and archived fields
        data = super().to_dict()
        data.update({
            "skillGroupID": self.skillGroupID,
            "resourceID": self.resourceID,
            "actual_minutes": self.actual_minutes,
            "status": self.status,
            "is_completed": self.is_completed,
            "completed_date": self.completed_date.isoformat(),
            "points_awarded": self.points_awarded
        })
        return data

# Added table for the combination between Resource (Engineer) and Skill Group
class Resource_SkillGroup(Resource, SkillGroup):
    # The combination between the Engineer and their skill group
    def __init__(self, id: str, skillGroupID: str, resourceID: str):
        self.id = id
        self.skillGroupID = skillGroupID
        self.resourceID = resourceID
    
    def to_dict(self): 
        return {"id": self.id, "skillGroupID": self.skillGroupID, "resourceID": self.resourceID}


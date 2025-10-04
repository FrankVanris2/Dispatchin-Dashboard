# Defining the Interface that will cause loose coupling
from abc import ABC, abstractmethod
from datetime import datetime
import uuid
import random


class ITicketRepository(ABC):
    """ Abstract class defining the contract for data access (Interface).
    This enables loose coupling and makes testing easy (by swapping the Mock with a real DB)

    """

    @abstractmethod
    def get_skill_groups(self) -> list[SkillGroup]:
        pass
    
    @abstractmethod
    def get_resources(self) -> list[Resource]:
        pass

    @abstractmethod
    def get_virtual_queue_tickets(self) -> list[VirtualQueueTicket]:
        pass

    @abstractmethod
    def get_ticket_by_id(self, ticket_id: str) -> VirtualQueueTicket:
        pass

    @abstractmethod
    def remove_ticket_from_queue(self, ticket_id: str):
        pass

    @abstractmethod
    def archive_ticket(self, ticket:ArchivedTicket):
        pass

    @abstractmethod
    def get_archived_tickets(self) ->list[ArchivedTicket]:
        pass

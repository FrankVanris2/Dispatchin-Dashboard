# Mock Repository for the foundation of the different tables that was given
from interfaces.data_repository import ITicketRepository
from models import SkillGroup, Resource, VirtualQueueTicket, ArchivedTicket
import random

# Tables VirtualQueueTicket, ArchivedTicket, SkillGroup, Resource, Resource_SkillGroup


# Create a function that generates mock data adhering to the ERD structure you were given ^^^^

# --- 3. Mock Implementation (The Concrete Mock Repository) ---
class MockTicketRepository(ITicketRepository):
    """ Concrete implementation using in-memory Python lists/dicts (Mocks). """

    def __init__(self):
        self._skill_groups = {}
        self._resources = {}
        self._queue = {}
        self._archive = []
        self._points_map = {
            'Line1': 100,
            'Line2': 200,
            'Line3': 300
        }
    
    def initialize_mock_data(self):
        """ Pre-populate data for demonstration. """
        self._skill_groups = {
            'L1': SkillGroup('L1', 'Line 1 (Easiest)', self._points_map['Line1']),
            'L2': SkillGroup('L2', 'Line 2 (Medium)', self._points_map['Line2']),
            'L3': SkillGroup('L3', 'Line 3 (Hardest)', self._points_map['Line3'])
        }
        self._resources = {
            'R001': Resource('R001', 'Adela Parkson'),
            'R002': Resource('R002', 'Christian Mad'),
            'R003': Resource('R003', 'Jason Statham')
        }

        # Adding some initial tickets to the queue (All randomized)
        for i in range(40):
            group_id = random.choice(['L1', 'L2', 'L3'])
            priority = random.randint(1, 5)
            ticket = VirtualQueueTicket(group_id, priority, random.randint(30, 120))
            self._queue[ticket.ticketID] = ticket

        for _ in range(15):
            group_id = random.choice(['L1', 'L2', 'L3'])
            engineer_id = random.choice(list(self._resources.keys()))
            points = self._points_map[self._skill_groups[group_id].name.split()[0]]

            # Create a dummy ticket to archive
            dummy_ticket = VirtualQueueTicket(group_id, 3, 60)
            archived = ArchivedTicket(dummy_ticket, engineer_id, points)
            self._archive.append(archived)
    
    def get_skill_groups(self) -> list[SkillGroup]:
        return list(self._skill_groups.values())
    
    def get_resources(self) -> list[Resource]:
        return list(self._resources.value())
    
    def get_virtual_queue_tickets(self) -> list[VirtualQueueTicket]:
        # Return sorted by priority (e.g., lower number is higher priority)
        return sorted(list(self._queue.values()), key=lambda t: t.priority)
    
    def get_ticket_by_id(self, ticket_id: str) -> VirtualQueueTicket:
        ticket = self._queue.get(ticket_id)
        if ticket is None:
            raise ValueError(f"Ticket ID {ticket_id} not found in queue")
        return ticket
    
    def remove_ticket_from_queue(self, ticket_id: str):
        if ticket_id in self._queue:
            del self._queue[ticket_id]
        else:
            raise ValueError(f"Ticket ID {ticket_id} not found in queue for removal")
        
    def archive_ticket(self, ticket: ArchivedTicket):
        self._archive.append(ticket)

    def get_archived_tickets(self) -> list[ArchivedTicket]:
        return self._archive
            

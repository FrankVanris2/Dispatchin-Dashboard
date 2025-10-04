# Mock Repository for the foundation of the different tables that was given
from interfaces.data_repository import ITicketRepository
from mockrepo.models import SkillGroup, Resource, VirtualQueueTicket, ArchivedTicket, Resource_SkillGroup
import random
import itertools

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
        self._resource_skill_groups = []
        self._points_map = {
            'Line1': 100,
            'Line2': 200,
            'Line3': 300
        }
    
    def initialize_mock_data(self):
        """ 
        Pre-populate data for demonstration. 
        Note: The Resource_SkillGroup table is populated based on the archived tickets.
        """
        self._skill_groups = {
            'L1': SkillGroup('L1', 'Line1 (Easiest)', self._points_map['Line1']),
            'L2': SkillGroup('L2', 'Line2 (Medium)', self._points_map['Line2']),
            'L3': SkillGroup('L3', 'Line3 (Hardest)', self._points_map['Line3'])
        }
        self._resources = {
            'R001': Resource('R001', 'Adela Parkson'),
            'R002': Resource('R002', 'Christian Mad'),
            'R003': Resource('R003', 'Jason Statham'),
            'R004': Resource('R004', 'Frank Vanris')
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
            archived = ArchivedTicket(dummy_ticket, group_id, engineer_id, points)
            self._archive.append(archived)

        # CRUCIAL STEP: populating Resource_SkillGroup based on archived tickets
        # This set will store unique (resourceID, skillGroupID) pairs
        inferred_skills = set()
        rsg_id_generator = itertools.count(1)

        for archived_ticket in self._archive:
            resource_id = archived_ticket.resourceID
            skill_group_id = archived_ticket.skillGroupID

            relationship_key = (resource_id, skill_group_id)

            if relationship_key not in inferred_skills:
                # The engineer has successfully closed a ticket for this skill group,
                # so we record this relationship
                inferred_skills.add(relationship_key)

                # Create the Resource_SkillGroup record with a unique ID
                new_rsg_id = f"RS{next(rsg_id_generator):03d}"
                rsg = Resource_SkillGroup(new_rsg_id, skill_group_id, resource_id)
                self._resource_skill_groups.append(rsg)

    
    def get_skill_groups(self) -> list[SkillGroup]:
        return list(self._skill_groups.values())
    
    def get_resources(self) -> list[Resource]:
        return list(self._resources.values())
    
    def get_resources_skillgroups(self) -> list[Resource_SkillGroup]:
        """ Returns the list of Resource_SkillGroup records (the M:M mapping). """
        return self._resource_skill_groups
    
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
            

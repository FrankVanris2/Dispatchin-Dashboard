# This is the Ticket Service (CORE Business Logic that is necessary)
from interfaces.data_repository import ITicketRepository
from mockrepo.models import ArchivedTicket

class TicketService:
    """ Handles the business logic: calculating points, moving data, and aggregation. """

    def __init__(self, repository: ITicketRepository):
        self._repo = repository

        #Pre-load the points system map from the skill group
        self._points_map = {sg.skillGroupID: sg.points for sg in self._repo.get_skill_groups()}

    def get_points_for_skill_group(self, skill_group_id: str) -> int:
        """ Implements the gamification logic (Line 1=100, Line 2=200, etc.). """
        # Mapping skill group IDs (e.g., 'L1') to point values (e.g., 100)
        points = int(skill_group_id[1:]) * 100 # Currently not the best solution so will need a change in the future
        return self._points_map.get(skill_group_id, points) # will need a change later
    
    def close_and_archive_ticket(self,ticket_id: str, resource_id: str) -> ArchivedTicket:
        """
        Critical function:
        1. Finds ticket.
        2. Calculate points.
        3. Creates ArchivedTicket object.
        4. Archives it.
        5. Removes it from the queue.
        """
        
        #1. Find the ticket
        ticket_to_close = self._repo.get_ticket_by_id(ticket_id)

        #2. Calculate points
        points = self.get_points_for_skill_group(ticket_to_close.skillGroupID)

        #3. Create archived record
        archived_ticket = ArchivedTicket(ticket_to_close, ticket_to_close.skillGroupID, resource_id, points)

        #4. Archive it
        self._repo.archive_ticket(archived_ticket)

        #5. Remove from queue
        self._repo.remove_ticket_from_queue(ticket_id)

        return archived_ticket

    def calculate_leaderboard(self) -> list:
        """Aggregates archived data to create the leaderboard scores. """
        archived_tickets = self._repo.get_archived_tickets()

        # Dictionary to store {resourceID: total_points}
        engineer_scores = {}
        engineer_tickets_solved = {}

        for ticket in archived_tickets:
            engineer_id = ticket.resourceID
            points = ticket.points_awarded

            # Aggregate Points
            engineer_scores[engineer_id] = engineer_scores.get(engineer_id, 0) + points

            # Aggregate Tickets Solved
            engineer_tickets_solved[engineer_id] = engineer_tickets_solved.get(engineer_id, 0) + 1

        # Formatting the output
        leaderboard_data = []
        for resource in self._repo.get_resources():
            resource_id = resource.resourceID
            leaderboard_data.append({
                "engineer_name": resource.name,
                "resourceID": resource_id,
                "total_points": engineer_scores.get(resource_id, 0),
                "tickets_solved": engineer_tickets_solved.get(resource_id, 0)
            })
        
        # Rank the results (highest points first)
        return sorted(leaderboard_data, key=lambda x: x['total_points'], reverse=True)        
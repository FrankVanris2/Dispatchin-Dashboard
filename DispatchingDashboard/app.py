# The Main Flask Server for the thing to run locally. Will do things through Azure later.

from flask import Flask, jsonify, request
from services.repositories.mock_repository import MockTicketRepository
from services.tickets_service import TicketService
from models import SkillGroup, Resource
import uuid
from datetime import datetime

# --- Dependency Injection Setup ---
# In a full application, the repository would be injected based on the environment (test/prod)
# For this proof-of-concept, we instantiate the mock repository directly
repository = MockTicketRepository()
ticket_service = TicketService(repository)

# --- Flask App Initialization ---
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """ Simple status check. """
    return jsonify({"status": "Dispatching Dashboard API Running", "message": "Backend logic is main focus"})

@app.route('/api/queue', methods=['GET'])
def get_queue():
    """GET endpoint to display the current tickets in the virtual queue."""
    queue_tickets = repository.get_virtual_queue_tickets()
    #Serialize the tickets to a list of dicts for JSON output
    serialized_tickets = [ticket.to_dict() for ticket in queue_tickets]
    return jsonify({"queue": serialized_tickets})

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    GET endpoint to display the gamified leaderboard.
    Calculates total points per engineer based on archived tickets.
    """
    leaderboard = ticket_service.calculate_leaderboard()
    return jsonify({"leaderboard": leaderboard})

@app.route('/api/close_ticket', methods=['POST'])
def close_ticket():
    """
    POST endpoint to simulate the critical event: closing a ticket.
    
    Expected JSON payload
    {
        "ticketID": "unique_ticket_id_from_queue",
        "resourceID": "R001"
    }
    """
    data = request.json

    if not data or 'ticketID' not in data or 'resourceID' not in data:
        return jsonify({"error": "Missing ticketID or resourceID in payload."}), 400
    
    ticket_id = data['ticketID']
    resource_id = data['resourceID']

    try:
        # This single call executes the core logic: move, calculate points, archive.
        archived_ticket = ticket_service.close_and_archive_ticket(ticket_id, resource_id)

        return jsonify({
            "success": True,
            "message": f"Ticket {ticket_id} closed by {resource_id}.",
            "points_awarded": archived_ticket.points_awarded
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        # General error handling for robustness
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    
# --- Test Button Endpoint (Crucial Deliverable), Testing purposes
@app.route('/api/simulate_closure', methods=['POST'])
def simulate_closure():
    """
    Endpoint to simulate the closure of the NEXT available ticket by a random engineer.
    This fulfills the 'Test Button' requirement.
    """
    queue_tickets = repository.get_virtual_queue_tickets()

    if not queue_tickets:
        return jsonify({"message": "No tickets left in the queue to simulate closure."}), 404
    
    # Select the first ticket in the queue for simulation
    ticket_to_close = queue_tickets[0]

    # Select a random engineer (R0001 or R002) forthe simulation
    engineers = repository.get_resources()
    resource_id = engineers[0].resourceID if len(engineers) > 0 else "R001" # Default engineer

    try: 
        archived_ticket = ticket_service.close_and_archive_ticket(ticket_to_close.ticketID, resource_id)

        return jsonify({
            "success": True,
            "message": f"SIMULATED: Ticket {ticket_to_close.ticketID} (SkillGroup: {ticket_to_close.SkillGroupID}) closed by {resource_id}.",
            "points_awarded": archived_ticket.points_awarded,
            "leaderboard_status": ticket_service.calculate_leaderboard()
        })
    except Exception as e:
        return jsonify({"error": f"Simulation failed: {e}"}), 500
    
if __name__ == '__main__':
    #Initialize some mock data for the queue when the app starts
    repository.initialize_mock_data()
    print("Mock data initialized. API is ready.")
    app.run(debug=True, port=5000)

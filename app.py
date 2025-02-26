from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

# In-memory storage for tickets
tickets = []
ticket_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    return jsonify(tickets)

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    global ticket_id_counter
    new_ticket = {
        'id': ticket_id_counter,
        'title': request.json['title'],
        'description': request.json['description'],
        'status': 'open'
    }
    tickets.append(new_ticket)
    ticket_id_counter += 1
    return jsonify(new_ticket), 201

@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket = next((ticket for ticket in tickets if ticket['id'] == ticket_id), None)
    if ticket is None:
        return jsonify({'error': 'Ticket not found'}), 404

    ticket['title'] = request.json.get('title', ticket['title'])
    ticket['description'] = request.json.get('description', ticket['description'])
    ticket['status'] = request.json.get('status', ticket['status'])
    return jsonify(ticket)

if __name__ == '__main__':
    app.run(debug=True)
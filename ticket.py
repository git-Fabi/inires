class Ticket:
    """
    Represents a ticket in the system.
    """
    def __init__(self, ticket_id, description):
        self.ticket_id = ticket_id
        self.description = description

    def to_dict(self):
        """
        Convert the ticket to a dictionary representation.
        """
        return {
            'ticket_id': self.ticket_id,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Ticket instance from a dictionary.
        :param data: A dictionary containing ticket data.
        """
        return cls(data['ticket_id'], data['description'])

# Additional methods and error handling can be implemented as needed.
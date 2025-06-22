def create_issue_reader_agent(self) -> FlockAgent:
    try:
        return FlockFactory.create_default_agent(
            name=self.name,
            description=self.description,
            input=Ticket.get_representation_for_agent(),
            output=TicketContext.get_representation_for_agent(),
            temperature=1.0,
            max_tokens=16384,
        )
    except Exception as e:
        # Log the exception or handle it as necessary
        print(f"Error creating issue reader agent: {e}")
        raise ValueError("Invalid input data structure")
import sys

class Ticket:
    def __init__(self, ticket_number, ticket_title, ticket_body):
        self.ticket_number = ticket_number
        self.ticket_title = ticket_title
        self.ticket_body = ticket_body

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: main.py <ticket_number> <ticket_title> <ticket_body>')
        sys.exit(1)

    ticket_number = sys.argv[1]
    ticket_title = sys.argv[2]
    ticket_body = sys.argv[3]

    ticket = Ticket(ticket_number, ticket_title, ticket_body)

    # Create the SolutionGeneratorAgent instance
    from solution_generator_agent import SolutionGeneratorAgent
    solution_generator_agent = SolutionGeneratorAgent()
    solution_generator_agent.create_solution_generator_agent()

    # Prepare the ticket context
    from ticket_context import TicketContext
    ticket_context = TicketContext(core_context='Summary of the ticket content.')

    # Invoke the runner function
    from runner import runner
    solution_plan = runner(ticket, ticket_context, solution_generator_agent)

    print(solution_plan)  # Print the generated solution plan
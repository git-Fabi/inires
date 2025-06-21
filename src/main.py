# The import for 'Ticket' is likely correct if 'src' is your content root.
from models.ticket import Ticket
# The import for your utils is now relative to its position inside 'src'.
from utils.utils_agents import setup_agents, runner


def main() -> str:
    """
    This is the main execution function.
    It sets up the application, creates test data, and runs the agent pipeline.
    """
    print("--- Preparing Test Ticket ---")

    sample_ticket = Ticket(
        ticket_title="Password Reset is not actually changing the password",
        ticket_body=(
            "The password reset email is being sent correctly, but after the user "
            "submits the new password, their old password still works. The password is not "
            "actually being updated. I think the issue might be in the `reset_password` "
            "function within `src/services/auth_service.py`."
        ),
        ticket_number="TICK-456"
    )

    print("--- Setting up Agents ---")
    inires_flock = setup_agents()

    print("--- Kicking off Agent Pipeline ---")
    # The runner receives the correctly instantiated ticket object.
    result = runner(inires_flock, ticket=sample_ticket)

    return result



if __name__ == "__main__":
    final_solution_plan = main()

    print("\n--- FINAL RESULT FROM PIPELINE ---")
    print(final_solution_plan)
    print("----------------------------------")
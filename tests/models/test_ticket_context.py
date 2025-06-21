from models.ticket_context import TicketContext  # Adjust import path as needed


def test_ticket_context_manual_assignment():
    context = TicketContext()

    # Manually set values
    context.ticket_id = "TCK-123"
    context.best_practices = "Follow SOLID principles."
    context.ticket_context = "This ticket addresses login failure handling."

    # Pytest assertions
    assert context.ticket_id == "TCK-123"
    assert context.best_practices == "Follow SOLID principles."
    assert context.ticket_context == "This ticket addresses login failure handling."


def test_get_representation_for_agent_contains_expected_fields():
    rep = TicketContext.get_representation_for_agent()

    # Use assert statements for all expectations (no unused value)
    assert isinstance(rep, str)
    assert "ticket_id: str" in rep
    assert "best_practices: str" in rep
    assert "ticket_context: str" in rep

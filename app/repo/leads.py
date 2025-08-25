import json
from app.models.lead import Lead


async def create_lead(
    session,
    client_id: int,
    source: str,
    zone: str,
    idea: str,
    size: str,
    work_type: str,
    references: list = None,
    comment: str = None,
):
    """Create a new lead entry."""
    references_json = json.dumps(references) if references else None
    lead = Lead(
        client_id=client_id,
        source=source,
        zone=zone,
        idea=idea,
        size=size,
        work_type=work_type,
        references_json=references_json,
        comment=comment,
        status="new",
    )
    session.add(lead)
    await session.flush()
    return lead

from app.schemas.transaction import TransactionEvent

_events: dict[str, TransactionEvent] = {}

def record_event(event: TransactionEvent) -> bool:
    if event.transaction_id in _events:
        return False
    _events[event.transaction_id] = event
    return True

def get_overview() -> dict:
    events = list(_events.values())
    total = len(events)
    successful = sum(e.status == "SUCCESS" for e in events)
    failed = sum(e.status == "FAILED" for e in events)
    pending = sum(e.status == "PENDING" for e in events)

    return {
        "total" : total,
        "successful_transactions" : successful,
        "failed_transactions" : failed,
        "pending_transactions" : pending,
        "success_rate" : round(successful / total * 100, 2) if total > 0 else 0.0,
    }



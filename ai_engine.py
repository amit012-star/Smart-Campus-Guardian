def analyze_emergency(emergency_type, description):

    text = (
        emergency_type + " " + description
    ).lower()

    if "fire" in text:
        return (
            "CRITICAL",
            "Immediately alert campus security and fire response team."
        )

    if "unconscious" in text:
        return (
            "CRITICAL",
            "Contact medical emergency services immediately."
        )

    if "bleeding" in text:
        return (
            "CRITICAL",
            "Provide emergency medical assistance immediately."
        )

    if "accident" in text:
        return (
            "CRITICAL",
            "Send medical assistance and secure the accident area."
        )

    if "danger" in text or "threat" in text:
        return (
            "CRITICAL",
            "Alert campus security and keep students away from the area."
        )

    if "injury" in text or "injured" in text:
        return (
            "IMPORTANT",
            "Contact the medical support team."
        )

    if "pain" in text or "medical" in text:
        return (
            "IMPORTANT",
            "Contact campus medical support."
        )

    if "security" in text:
        return (
            "IMPORTANT",
            "Notify campus security for assistance."
        )

    return (
        "NORMAL",
        "Review the report and take appropriate action."
  )

"""Context Augmented Generation helpers."""


def apply_context(user_id, question, base_answer, context_items):
    """Return an answer enriched with the user's stored context.

    The function keeps the original RAG answer intact and adds a visible
    context section only when usable context exists.
    """
    usable_context = []

    for item in context_items or []:
        key = str(item.get("key", "")).strip()
        value = item.get("value")

        if key and value is not None and str(value).strip():
            usable_context.append({"key": key, "value": value})

    if not usable_context:
        return base_answer

    context_summary = "; ".join(
        f"{item['key']}: {item['value']}" for item in usable_context
    )

    return (
        f"{base_answer}\n\n"
        f"Contexto aplicado para {user_id}: {context_summary}. "
        "La respuesta anterior debe interpretarse tomando en cuenta ese contexto."
    )
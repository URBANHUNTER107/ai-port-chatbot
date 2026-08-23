def format_value(value):
    """
    Convert nested dictionaries/lists into readable text.
    """

    if isinstance(value, dict):

        parts = []

        for key, val in value.items():

            readable_key = key.replace("_", " ").title()

            parts.append(
                f"{readable_key}: {format_value(val)}"
            )

        return " | ".join(parts)

    elif isinstance(value, list):

        return ", ".join(
            format_value(item)
            for item in value
        )

    else:

        return str(value)


def create_chunk(chunk_id, category, title, content):
    """
    Create one standardized RAG chunk.
    """

    return {
        "id": chunk_id,
        "category": category,
        "title": title,
        "text": (
            f"{title}. "
            f"{format_value(content)}"
        )
    }


def looks_like_a_list_of_things(value):
    """
    Decides whether a section should be split into multiple chunks
    (one per item) or kept as a single chunk.

    - A dict counts as "a list of things" if EVERY value inside it
      is also a dict. Example: {"project_1": {...}, "project_2": {...}}

    - A list counts as "a list of things" if EVERY item inside it
      is a dict. Example: [{"name": "X"}, {"name": "Y"}]
    """

    if isinstance(value, dict) and len(value) > 0:
        return all(isinstance(v, dict) for v in value.values())

    if isinstance(value, list) and len(value) > 0:
        return all(isinstance(v, dict) for v in value)

    return False


def pick_a_title(key, sub_value):
    """
    When a section gets split into multiple chunks, each chunk needs
    a readable title. We check a few common field names first, and
    fall back to the dictionary key itself if none of them exist.
    """

    if isinstance(sub_value, dict):
        for possible_title_field in ["name", "title", "role", "event", "program"]:
            if sub_value.get(possible_title_field):
                return sub_value[possible_title_field]

    return str(key).replace("_", " ").title()


def create_chunks(data):
    """
    Walks through every top-level section of personal_data.json and
    chunks it using consistent rules instead of a separate hand-written
    block per section.
    """

    chunks = []

    for key, value in data.items():

        if looks_like_a_list_of_things(value):
            # This section is really multiple separate items -> one chunk each

            items = value.items() if isinstance(value, dict) else enumerate(value)

            for sub_key, sub_value in items:

                title = pick_a_title(sub_key, sub_value)

                chunks.append(
                    create_chunk(
                        chunk_id=f"{key}_{sub_key}",
                        category=key,
                        title=title,
                        content=sub_value
                    )
                )

        elif isinstance(value, dict) and len(value) > 1:
            # This section is a flat dict with several separate facts
            # (like about_me, personal_information, skills). Split it
            # field by field instead of mashing everything into one
            # giant chunk - a big "keyword soup" chunk ends up vaguely
            # matching almost every query, which crowds out chunks
            # that should actually win.

            for field_key, field_value in value.items():

                chunks.append(
                    create_chunk(
                        chunk_id=f"{key}_{field_key}",
                        category=key,
                        title=f"{key.replace('_', ' ').title()} - {field_key.replace('_', ' ').title()}",
                        content=field_value
                    )
                )

        else:
            # This section is just one single piece of info -> single chunk

            chunks.append(
                create_chunk(
                    chunk_id=key,
                    category=key,
                    title=key.replace("_", " ").title(),
                    content=value
                )
            )

    return chunks
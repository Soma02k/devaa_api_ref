import math

def paginate_query(query, page: int = 1, limit: int = 10):
    """
    Reusable global pagination utility function.
    
    :param query: SQLAlchemy Query object
    :param page: Current page number (1-indexed)
    :param limit: Number of items per page
    :return: dict containing items serialized via to_dict() and pagination metadata
    """
    try:
        page = int(page)
        limit = int(limit)
    except (ValueError, TypeError):
        raise ValueError("Page and limit parameters must be integers")

    if page < 1:
        raise ValueError("Page parameter must be greater than or equal to 1")

    if limit < 1:
        raise ValueError("Limit parameter must be greater than or equal to 1")

    total = query.count()
    offset = (page - 1) * limit
    records = query.offset(offset).limit(limit).all()

    items = [record.to_dict() for record in records]
    total_pages = math.ceil(total / limit) if total > 0 else 0

    return {
        "items": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages
        }
    }

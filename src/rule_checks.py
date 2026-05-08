import pandas as pd

def is_missing(value):
    return pd.isna(value) or str(value).strip() == ""

def run_rule_checks(row):

    issues = []

    # Required fields
    required_fields = [
        "event_id"
    ]

    # Optional fields (only checked if present)
    possible_required_fields = [
        "title",
        "name",
        "description",
        "summary",
        "event_type",
        "category",
        "source_url",
        "url",
        "market",
        "country",
        "event_date",
        "published_at",
        "created_at"
    ]

    # Add available fields
    for field in possible_required_fields:
        if field in row:
            required_fields.append(field)

    # Missing value checks
    for field in required_fields:

        if field in row and is_missing(row[field]):

            issues.append({
                "check_name": f"missing_{field}",
                "check_type": "rule",
                "verdict": "fail",
                "reason": f"{field} is missing"
            })

    # URL validation
    for url_field in ["source_url", "url", "link"]:

        if url_field in row and not is_missing(row[url_field]):

            url = str(row[url_field])

            if not url.startswith(("http://", "https://")):

                issues.append({
                    "check_name": f"invalid_{url_field}",
                    "check_type": "rule",
                    "verdict": "fail",
                    "reason": f"{url_field} is not a valid URL"
                })

    # Date validation
    for date_field in [
        "event_date",
        "published_at",
        "created_at",
        "updated_at"
    ]:

        if date_field in row and not is_missing(row[date_field]):

            try:
                pd.to_datetime(row[date_field])

            except Exception:

                issues.append({
                    "check_name": f"invalid_{date_field}",
                    "check_type": "rule",
                    "verdict": "fail",
                    "reason": f"{date_field} is not a valid date"
                })

    return issues
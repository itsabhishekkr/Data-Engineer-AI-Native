# News Events Quality Check Skill

## Purposes

This skill checks the quality of news event records using both rule-based checks and LLM-based checks.

## When to use

Use this skill when ingesting, validating, or reviewing a batch of news event records.

## Required input

A CSV file with these columns:

- event_id
- title
- description
- event_type
- company_name
- person_name
- source_url
- market
- event_date

## Checks

### Rule-based checks

- Missing required fields
- Invalid URL
- Invalid market
- Duplicate event_id
- Invalid date

### LLM-based checks

- Semantic accuracy
- Entity resolution
- Source credibility and relevance

## Output

The skill returns:

```json
{
  "record_id": "evt_001",
  "verdict": "fail",
  "failed_checks": ["semantic_accuracy"],
  "reason": "Event type does not match description",
  "confidence": 0.86,
  "suggested_action": "change_event_type"
}
```
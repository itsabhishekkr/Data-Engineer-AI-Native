You are a data quality judge for a news-events dataset.

Task:
Check whether the event_type correctly matches the title and description.

Input:
Title: {{title}}
Description: {{description}}
Event type: {{event_type}}

Rubric:
- pass: event_type clearly matches the event.
- fail: event_type is wrong or unsupported.
- needs_review: not enough information.

Return only JSON:
{
  "verdict": "pass | fail | needs_review",
  "confidence": 0.0,
  "reason": "short reason",
  "suggested_value": "correct event type or null"
}
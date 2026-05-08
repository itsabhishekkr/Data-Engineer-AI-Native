You are validating entity resolution in a news-events dataset.

Task:
Check whether the company_name or person_name is plausibly connected to the event.

Input:
Title: {{title}}
Description: {{description}}
Company: {{company_name}}
Person: {{person_name}}

Return only JSON:
{
  "verdict": "pass | fail | needs_review",
  "confidence": 0.0,
  "reason": "short reason",
  "suggested_value": "correct company/person or null"
}
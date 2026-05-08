You are checking source credibility and relevance.

Task:
Decide whether this looks like a real relevant news event or low-quality noise.

Input:
Title: {{title}}
Description: {{description}}
Source URL: {{source_url}}

Return only JSON:
{
  "verdict": "pass | fail | needs_review",
  "confidence": 0.0,
  "reason": "short reason",
  "suggested_value": null
}
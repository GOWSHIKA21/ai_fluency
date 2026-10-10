# Day 8 Task Results

## Part A — Placement Policy
- Placement search top result: `placement_policy.md`
- Placement question score: 0.170
- Eligibility: CGPA 6.5 or above with no standing arrears.

## Part B — Exam Eligibility Tool

| Attendance | Result | Correct? |
|---|---|---|
| 82% | ELIGIBLE | Yes |
| 70% | CONDONATION, Rs. 500 per course | Yes |
| 50% | NOT ELIGIBLE | Yes |
| 120% | ERROR: Attendance must be between 0 and 100 | Yes |

## Part C — Relevance Guard
- MAX_DISTANCE: 0.6
- Placement score: 0.170
- France similarity scores: Pending measurement

## Part D — Agent Test Results

| # | Tools called | Agent's answer | Correct? |
|---|---|---|---|
| 1 | search_handbook | CGPA 6.5 or above; no standing arrears | Y |
| 2 | check_exam_eligibility | Condonation, Rs. 500 per course | Y |
| 3 | get_course_fee × 2, calculator | Rs. 32,000 | Y |
| 4 | calculator | Rs. 30,500 | Y |
| 5 | None | Not covered in the handbook | Y |

## Configuration
- Model used: Fill in your configured model
- Embedding model: `BAAI/bge-small-en-v1.5`
- MAX_DISTANCE: 0.6
- France score: Pending measurement

## Notes
All five questions ran in thread `task-run`. The agent saved 22 messages. The France response was appropriate, but the relevance guard still needs direct verification.

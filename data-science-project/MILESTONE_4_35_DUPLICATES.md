# Milestone 4.35 — Identifying and Removing Duplicate Records

## Deliverable prepared
- Notebook: `notebooks/4_35_identifying_removing_duplicates.ipynb`

## What this notebook covers
1. Creates a DataFrame with exact and partial duplicates
2. Detects duplicates using `duplicated()`
3. Inspects duplicate rows
4. Removes duplicates using `drop_duplicates()`
5. Verifies results using shape comparison and re-check counts

## Suggested 2-minute video flow
1. Open notebook and state objective (duplicate handling).
2. Run the data-loading cell and show initial shape.
3. Run duplicate-detection cells and show duplicate rows.
4. Run deduplication cell and explain `keep='first'` vs `keep='last'`.
5. Run verification cell and show before/after shapes and remaining duplicate counts.
6. Close by explaining why deduplication improves data quality.

## Notes
- No modeling or visualization is included.
- Deduplication decisions are explicit and explainable.

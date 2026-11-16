-- % of scores worse than expected by state (30+ scores so small states don't skew it)
SELECT state,
       COUNT(DISTINCT facility_id) AS hospitals,
       COUNT(*) AS scores,
       ROUND(AVG(worse_than_expected) * 100, 1) AS pct_worse
FROM readmissions
GROUP BY state
HAVING COUNT(*) >= 30
ORDER BY pct_worse DESC;

-- which conditions have the most readmission problems
SELECT condition,
       COUNT(*) AS hospitals,
       ROUND(AVG(predicted_readmission_rate), 1) AS avg_readmit_rate,
       ROUND(AVG(worse_than_expected) * 100, 1) AS pct_worse,
       ROUND(SUM(CASE WHEN excess_readmissions > 0 THEN excess_readmissions ELSE 0 END)) AS excess_readmissions
FROM readmissions
GROUP BY condition
ORDER BY excess_readmissions DESC;

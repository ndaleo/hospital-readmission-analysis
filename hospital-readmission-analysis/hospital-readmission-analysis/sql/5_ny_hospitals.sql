-- NY hospitals worse than expected on 3 or more conditions
SELECT facility_name,
       COUNT(*) AS conditions_scored,
       SUM(worse_than_expected) AS conditions_worse,
       ROUND(AVG(excess_readmission_ratio), 3) AS avg_ratio
FROM readmissions
WHERE state = 'NY'
GROUP BY facility_id, facility_name
HAVING SUM(worse_than_expected) >= 3
ORDER BY conditions_worse DESC, avg_ratio DESC;

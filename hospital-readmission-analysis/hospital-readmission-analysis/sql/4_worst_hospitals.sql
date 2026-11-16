-- hospitals worse than expected on every condition they were scored on (at least 4)
SELECT facility_name,
       state,
       COUNT(*) AS conditions_scored,
       ROUND(AVG(excess_readmission_ratio), 3) AS avg_ratio
FROM readmissions
GROUP BY facility_id, facility_name, state
HAVING COUNT(*) >= 4 AND SUM(worse_than_expected) = COUNT(*)
ORDER BY avg_ratio DESC;

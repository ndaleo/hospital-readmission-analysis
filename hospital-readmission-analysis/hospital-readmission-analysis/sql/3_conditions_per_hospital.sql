-- how many conditions each hospital is worse than expected on
SELECT conditions_worse,
       COUNT(*) AS hospitals
FROM (
    SELECT facility_id, SUM(worse_than_expected) AS conditions_worse
    FROM readmissions
    GROUP BY facility_id
)
GROUP BY conditions_worse
ORDER BY conditions_worse;

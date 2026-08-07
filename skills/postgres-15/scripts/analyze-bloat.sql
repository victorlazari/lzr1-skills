-- Deterministic SQL script to identify bloated tables and indexes
-- Uses heuristic queries based on pg_class and pg_statistic

-- Note: For precise bloat analysis, the pgstattuple extension is recommended.
-- This script uses a heuristic approach that does not require extensions but provides a good estimate.

WITH constants AS (
    SELECT current_setting('block_size')::numeric AS bs, 23 AS hdr, 8 AS ma
),
bloat_info AS (
    SELECT
        schemaname, tablename, reltuples, relpages, bs,
        CEIL((cc.reltuples * ((datahdr + ma - (CASE WHEN datahdr%ma=0 THEN ma ELSE datahdr%ma END))+nullhdr2+4))/(bs-20::float)) AS est_pages
    FROM (
        SELECT
            ma,bs,schemaname,tablename,
            (datawidth+(hdr+ma-(case when hdr%ma=0 THEN ma ELSE hdr%ma END)))::numeric AS datahdr,
            (maxfracsum*(nullhdr+ma-(case when nullhdr%ma=0 THEN ma ELSE nullhdr%ma END))) AS nullhdr2
        FROM (
            SELECT
                schemaname, tablename, hdr, ma, bs,
                SUM((1-null_frac)*avg_width) AS datawidth,
                MAX(null_frac) AS maxfracsum,
                hdr+(
                    SELECT 1+count(*)/8
                    FROM pg_stats s2
                    WHERE null_frac<>0 AND s2.schemaname = s.schemaname AND s2.tablename = s.tablename
                ) AS nullhdr
            FROM pg_stats s, constants
            GROUP BY 1,2,3,4,5
        ) AS foo
    ) AS rs
    JOIN pg_class cc ON cc.relname = rs.tablename
    JOIN pg_namespace nn ON cc.relnamespace = nn.oid AND nn.nspname = rs.schemaname AND nn.nspname <> 'information_schema'
)
SELECT
    schemaname, tablename,
    reltuples::bigint AS table_rows,
    relpages::bigint AS table_pages,
    est_pages::bigint AS estimated_pages,
    CASE
        WHEN relpages < est_pages THEN 0
        ELSE relpages - est_pages
    END::bigint AS bloat_pages,
    CASE
        WHEN relpages < est_pages THEN 0
        ELSE bs * (relpages - est_pages)
    END::bigint AS bloat_size_bytes,
    CASE
        WHEN relpages = 0 THEN 0
        WHEN relpages < est_pages THEN 0
        ELSE ROUND(100 * (relpages - est_pages)::numeric / relpages::numeric, 2)
    END AS bloat_ratio
FROM bloat_info
ORDER BY bloat_size_bytes DESC
LIMIT 20;

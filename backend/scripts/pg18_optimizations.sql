-- PostgreSQL 18 Performance Optimizations for Climate Connect
-- Run with: psql -U ali -d climateconnect -f scripts/pg18_optimizations.sql

-- ============================================================================
-- COVERING INDEXES (PostgreSQL 11+, optimized for PG18)
-- Include extra columns to enable index-only scans, avoiding table lookups
-- ============================================================================

-- Project covering index for browse page
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_project_browse_covering 
ON organization_project (id DESC) 
INCLUDE (url_slug, image, thumbnail_image, project_type, start_date, end_date, loc_id)
WHERE is_draft = false AND is_active = true;

-- Organization covering index for browse page
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_organization_browse_covering
ON organization_organization (id DESC)
INCLUDE (name, url_slug, image, thumbnail_image, short_description, location_id);

-- ============================================================================
-- PARTIAL INDEXES (Smaller indexes for filtered queries)
-- ============================================================================

-- Active projects only (much smaller than full table index)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_project_active_partial
ON organization_project (created_at DESC)
WHERE is_draft = false AND is_active = true;

-- ============================================================================
-- BRIN INDEXES (Very small, great for large tables with sequential data)
-- ============================================================================

-- BRIN index on created_at for time-range queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_project_created_brin
ON organization_project USING BRIN (created_at);

-- ============================================================================
-- GIN INDEXES (Full-text search optimization)
-- ============================================================================

-- Full-text search on project names (if not exists)
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_project_name_gin
-- ON organization_project USING GIN (to_tsvector('english', name));

-- ============================================================================
-- EXPRESSION INDEXES
-- ============================================================================

-- Lower-case URL slug for case-insensitive lookups
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_project_url_slug_lower
ON organization_project (lower(url_slug));

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_organization_url_slug_lower
ON organization_organization (lower(url_slug));

-- ============================================================================
-- ANALYZE tables to update statistics
-- ============================================================================

ANALYZE organization_project;
ANALYZE organization_organization;
ANALYZE hubs_hub;
ANALYZE climateconnect_api_userprofile;

-- ============================================================================
-- Verify settings are applied
-- ============================================================================

SELECT name, setting, unit 
FROM pg_settings 
WHERE name IN (
    'shared_buffers', 
    'work_mem', 
    'effective_io_concurrency',
    'random_page_cost',
    'max_parallel_workers',
    'max_parallel_workers_per_gather',
    'jit',
    'default_statistics_target'
);

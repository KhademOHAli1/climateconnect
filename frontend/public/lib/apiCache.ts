/**
 * Simple in-memory cache for API responses
 * Complements backend caching by reducing redundant requests
 */

interface CacheEntry<T> {
  data: T
  timestamp: number
  ttl: number
}

class ApiCache {
  private cache: Map<string, CacheEntry<unknown>> = new Map()
  
  // Default TTL values (in milliseconds) - aligned with backend cache times
  static readonly TTL = {
    FAQ: 60 * 60 * 1000,        // 1 hour (matches backend)
    HUBS: 5 * 60 * 1000,        // 5 minutes (matches backend)
    SECTORS: 5 * 60 * 1000,     // 5 minutes (matches backend)
    SKILLS: 5 * 60 * 1000,      // 5 minutes
    PROJECT_TYPES: 60 * 60 * 1000,  // 1 hour
    DEFAULT: 60 * 1000,         // 1 minute
  } as const

  /**
   * Get cached data if valid, otherwise return undefined
   */
  get<T>(key: string): T | undefined {
    const entry = this.cache.get(key) as CacheEntry<T> | undefined
    if (!entry) return undefined

    const now = Date.now()
    if (now - entry.timestamp > entry.ttl) {
      // Cache expired, remove it
      this.cache.delete(key)
      return undefined
    }

    return entry.data
  }

  /**
   * Set cache with TTL
   */
  set<T>(key: string, data: T, ttl: number = ApiCache.TTL.DEFAULT): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl,
    })
  }

  /**
   * Check if cache entry exists and is valid
   */
  has(key: string): boolean {
    return this.get(key) !== undefined
  }

  /**
   * Remove a specific cache entry
   */
  delete(key: string): boolean {
    return this.cache.delete(key)
  }

  /**
   * Clear all cache entries
   */
  clear(): void {
    this.cache.clear()
  }

  /**
   * Clear expired entries (call periodically if needed)
   */
  cleanup(): void {
    const now = Date.now()
    for (const [key, entry] of this.cache.entries()) {
      if (now - entry.timestamp > entry.ttl) {
        this.cache.delete(key)
      }
    }
  }

  /**
   * Get cache key for API endpoint
   */
  static getCacheKey(url: string, locale?: string): string {
    return locale ? `${locale}:${url}` : url
  }
}

// Singleton instance
export const apiCache = new ApiCache()

// Export TTL constants for convenience
export const CACHE_TTL = ApiCache.TTL

/**
 * Helper to determine TTL based on URL pattern
 */
export function getTtlForUrl(url: string): number {
  if (url.includes('/faq')) return CACHE_TTL.FAQ
  if (url.includes('/hubs') || url.includes('/sector-hubs')) return CACHE_TTL.HUBS
  if (url.includes('/sectors')) return CACHE_TTL.SECTORS
  if (url.includes('/skills')) return CACHE_TTL.SKILLS
  if (url.includes('/project_types')) return CACHE_TTL.PROJECT_TYPES
  return CACHE_TTL.DEFAULT
}

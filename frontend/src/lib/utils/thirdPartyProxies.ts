import { createProxyHandler } from './proxyUtils';
import type { RequestHandler } from '@sveltejs/kit';

/**
 * Creates a simple prefix-stripping proxy handler.
 * Removes a prefix from the URL path and forwards to a target domain.
 *
 * @param prefix - The URL prefix to strip (e.g., '/mixpanel')
 * @param targetDomain - The target domain to proxy to (e.g., 'https://api.mixpanel.com')
 * @returns A RequestHandler that proxies requests
 *
 * @example
 * ```typescript
 * // In routes/(no-auth)/mixpanel/+server.ts
 * const handler = createPrefixProxy('/mixpanel', 'https://api.mixpanel.com');
 * export const GET = handler;
 * export const POST = handler;
 * ```
 */
export function createPrefixProxy(prefix: string, targetDomain: string): RequestHandler {
	return createProxyHandler({
		getDestinationUrl: (url) => {
			const pathname = url.pathname.replace(new RegExp(`^${prefix}`), '');
			return `${targetDomain}${pathname}${url.search}`;
		}
	});
}

/**
 * Pre-configured proxy handlers for common third-party services.
 *
 * To use these, create a +server.ts file in the appropriate route and export the handler:
 *
 * @example
 * ```typescript
 * // In routes/(no-auth)/mixpanel/+server.ts
 * import type { RequestHandler } from '@sveltejs/kit';
 * import { ThirdPartyProxies } from '$lib/utils/thirdPartyProxies';
 *
 * const handler = ThirdPartyProxies.mixpanel();
 *
 * export const GET: RequestHandler = handler;
 * export const POST: RequestHandler = handler;
 * export const PATCH: RequestHandler = handler;
 * export const PUT: RequestHandler = handler;
 * export const DELETE: RequestHandler = handler;
 * export const OPTIONS: RequestHandler = handler;
 * export const HEAD: RequestHandler = handler;
 * ```
 */
export const ThirdPartyProxies = {
	/**
	 * Creates a PostHog analytics proxy handler
	 * Route: /posthog/* -> https://app.posthog.com/*
	 */
	posthog: () => createPrefixProxy('/posthog', 'https://app.posthog.com'),

	/**
	 * Creates a Sentry error reporting proxy handler
	 * Extracts project ID from DSN and routes to Sentry's envelope endpoint
	 * Route: /sentry/* -> https://sentry.io/api/{projectId}/envelope/
	 */
	sentry: (dsn: string) =>
		createProxyHandler({
			getDestinationUrl: (_url, _request) => {
				const dsnUrl = new URL(dsn);
				const projectId = dsnUrl.pathname.replace(/^\/|\/$/g, '');
				return `https://sentry.io/api/${projectId}/envelope/`;
			}
		})
};

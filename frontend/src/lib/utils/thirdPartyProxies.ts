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
	 * Creates a Mixpanel proxy handler
	 * Route: /mixpanel/* -> https://api.mixpanel.com/*
	 */
	mixpanel: () => createPrefixProxy('/mixpanel', 'https://api.mixpanel.com'),

	/**
	 * Creates a Google Analytics proxy handler
	 * Route: /ga/* -> https://www.google-analytics.com/*
	 */
	googleAnalytics: () => createPrefixProxy('/ga', 'https://www.google-analytics.com'),

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
		}),

	/**
	 * Creates a Plausible Analytics proxy handler with domain injection
	 */
	plausible: (domain: string) =>
		createProxyHandler({
			getDestinationUrl: (url) => {
				if (url.pathname.includes('/api/event')) {
					return 'https://plausible.io/api/event';
				}
				return `https://plausible.io/js/script.js`;
			},
			transformRequest: async (request) => {
				// Add the domain to Plausible events
				if (request.method === 'POST') {
					const body = await request.text();
					const data = JSON.parse(body);
					data.domain = domain;
					return new Request(request, {
						body: JSON.stringify(data)
					});
				}
				return request;
			}
		}),

	/**
	 * Creates a Stripe webhook proxy handler with signature verification
	 * Note: This is just an example - you'd need to implement actual signature verification
	 */
	stripeWebhooks: (_endpointSecret: string) =>
		createProxyHandler({
			getDestinationUrl: (_url) => {
				// This would forward to your internal webhook handler
				return 'http://localhost:8000/webhooks/stripe';
			},
			transformRequest: async (request) => {
				// Verify Stripe signature before forwarding
				const signature = request.headers.get('stripe-signature');
				if (!signature) {
					throw new Error('Missing Stripe signature');
				}
				// TODO: Implement actual signature verification using _endpointSecret
				return request;
			}
		})
};

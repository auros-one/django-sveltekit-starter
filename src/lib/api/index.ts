/**
 * We are using openapi-fetch to generate typescript client for our backend API.
 * https://openapi-ts.pages.dev/openapi-fetch/
 *
 * Update the types by syncing the schema from backend:
 * > npm run sync-types
 */
import createClient, { type Middleware } from 'openapi-fetch';
import type { paths } from './backend-api-schema.d.ts';
import { waitForJWT } from '$lib/stores/auth';

const apiClient = createClient<paths>({ baseUrl: '/api' }); // api request are proxied through /api

/**
 * Middleware to add JWT token to the request headers
 */
const UNPROTECTED_ROUTES = [
	'/api/accounts/signup/',
	'/api/accounts/login/',
	'/api/accounts/token/refresh/',
	'/api/accounts/password/reset/',
	'/api/accounts/password/reset/confirm/'
];
const addJWT: Middleware = {
	async onRequest({ request }) {
		// don't modify request for unprotected routes
		const url = new URL(request.url);
		if (UNPROTECTED_ROUTES.some((route) => url.pathname.startsWith(route))) {
			return undefined;
		}

		// Create new headers to avoid modifying the original
		const headers = new Headers(request.headers);
		const jwt = await waitForJWT();
		headers.set('Authorization', `Bearer ${jwt}`);

		// Create a new request instead of cloning
		return new Request(request.url, {
			method: request.method,
			headers,
			body: request.body,
			credentials: request.credentials,
			mode: request.mode,
			referrer: request.referrer
		});
	}
};
apiClient.use(addJWT);

export { apiClient };

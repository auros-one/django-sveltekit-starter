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
	'/api/accounts/token/refresh/'
];
const addJWT: Middleware = {
	async onRequest({ request }) {
		// don’t modify request for unprotected routes
		const url = new URL(request.url);
		if (UNPROTECTED_ROUTES.some((route) => url.pathname.startsWith(route))) {
			console.log('addJWT UNPROTECTED_ROUTES', url.pathname);
			return undefined;
		}

		// add JWT token to the request headers
		const clonedRequest = request.clone();
		const jwt = await waitForJWT();
		clonedRequest.headers.set('Authorization', `Bearer ${jwt}`);
		return clonedRequest;
	}
};
apiClient.use(addJWT);

/**
 * Middleware to throw an error if the response status is 4xx or 5xx
 */
const throwOnError: Middleware = {
	async onResponse({ response }) {
		if (response.status >= 400) {
			const body = response.headers.get('content-type')?.includes('json')
				? JSON.stringify(await response.clone().json())
				: await response.clone().text();
			throw new Error(body);
		}
		return undefined;
	}
};
apiClient.use(throwOnError);

export { apiClient };

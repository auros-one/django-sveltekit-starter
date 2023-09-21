/**
 * We using openapi-fetch to generate typescript client for our backend API.
 * https://openapi-ts.pages.dev/openapi-fetch/
 *
 * Update the types by syncing the schema from backend:
 * > npm run sync-types
 */
import createClient from 'openapi-fetch';
import type { paths } from './backend-api-schema.d.ts';

const apiClient = createClient<paths>({ baseUrl: '/api' }); // api request are proxied through /api

export { apiClient };

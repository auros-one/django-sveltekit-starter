import { error } from '@sveltejs/kit';
import { PUBLIC_BASE_API_URL } from '$env/static/public';
import type { RequestHandler } from './$types';

export const GET = (async ({ cookies, fetch, url: _url }) => {
	try {
		// refresh-token cookie is required
		const refreshToken = cookies.get('refresh-token');
		if (refreshToken === undefined) error(401);

		// get new JWT using the refresh token
		const response = await fetch(PUBLIC_BASE_API_URL + '/api/accounts/token/refresh/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ refresh: refreshToken })
		});

		if (!response.ok) {
			cookies.delete('refresh-token', { path: '/' });
			error(401);
		}
		return response;
	} catch (err) {
		cookies.delete('refresh-token', { path: '/' });
		error(500, `${err}`);
	}
}) satisfies RequestHandler;

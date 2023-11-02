/**
 * Server-side check for the refresh-token cookie.
 * If it is present, redirect to the user homepage.
 */
import { redirect } from '@sveltejs/kit';

import type { PageServerLoad } from './$types';

export const load = (async ({ cookies }) => {
	const refreshToken = cookies.get('refresh-token');
	if (refreshToken !== undefined) throw redirect(302, '/');
}) satisfies PageServerLoad;

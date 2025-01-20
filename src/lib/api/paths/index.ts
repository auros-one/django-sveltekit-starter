import { PUBLIC_BASE_API_URL } from '$env/static/public';

export function makeAPIPath(path: string): string {
	/**
	 * Requests to the backend API are proxied through the SvelteKit server at `/api`.
	 */
	return `/api${path}`;
}

export const apiPath = {
	accounts: {
		user: makeAPIPath('/accounts/user/'),
		signup: makeAPIPath('/accounts/signup/'),
		verify_email: makeAPIPath('/accounts/signup/verify-email/'),
		resend_email: makeAPIPath('/accounts/signup/resend-email/'),
		login: makeAPIPath('/accounts/login/'),
		// This endpoint is called from the server, so it doesn't need to be proxied
		refresh: PUBLIC_BASE_API_URL + '/api/accounts/token/refresh/',
		logout: makeAPIPath('/accounts/logout/'),
		password_change: makeAPIPath('/accounts/password/change/'),
		password_reset: makeAPIPath('/accounts/password/reset/'),
		password_reset_confirm: makeAPIPath('/accounts/password/reset/confirm/')
	}
};

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
		refresh: makeAPIPath('/accounts/token/refresh/'),
		logout: makeAPIPath('/accounts/logout/'),
		password_change: makeAPIPath('/accounts/password/change/')
	}
};

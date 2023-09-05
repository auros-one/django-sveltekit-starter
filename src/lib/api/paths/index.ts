import { PUBLIC_BASE_API_URL } from '$env/static/public';

export function makeAPIPath(path: string): string {
	return `${PUBLIC_BASE_API_URL}${path}`;
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

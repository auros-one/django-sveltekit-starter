import { apiPath } from '$lib/api/paths';
import { waitForJWT } from '$lib/stores/auth';
import { user, type User } from '$lib/stores/account';

export async function getUser() {
	const response = await fetch(apiPath.accounts.user, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + (await waitForJWT())
		},
		credentials: 'include'
	});
	const data = await response.json();

	user.set(data as User);
}

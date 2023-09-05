import { apiPath } from '$lib/api/paths';
import { jwt } from '$lib/stores/auth';
import { user } from '$lib/stores/account';
import { get } from 'svelte/store';

export async function getUser() {
	const jwtToken = get(jwt);
	if (jwtToken === undefined) throw new Error('No jwt token');

	const response = await fetch(apiPath.accounts.user, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: 'Bearer ' + jwtToken
		},
		credentials: 'include'
	});
	const data = await response.json();

	user.set(data);
}

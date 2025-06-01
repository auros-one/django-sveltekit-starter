import { user, type User } from '$lib/stores/account';
import { apiClient } from '$lib/api';

export async function getUser() {
	const { data } = await apiClient.GET('/accounts/user/');
	if (data) {
		user.set(data as User);
	}
}

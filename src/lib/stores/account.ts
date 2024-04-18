import { persisted } from '$lib/stores/cookieStore';

export interface User {
	email: string;
	verified: boolean;
}

export const user = persisted<User>('user', null);

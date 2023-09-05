import { writable } from 'svelte/store';

export interface User {
	email: string;
	verified: boolean;
}

export const user = writable<User | undefined>(undefined);

import { persisted } from '$lib/stores/utils/cookieStore';
import type { components } from '$lib/api/schema';

export type User = components['schemas']['UserDetails'];

export const user = persisted<User>('user', null);

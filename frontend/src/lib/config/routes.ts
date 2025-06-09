/**
 * Centralized navigation configuration
 * This makes it easy to manage routes across different components
 */

export interface NavigationRoute {
	name: string;
	href: string;
	icon?: string;
	subroutes?: Array<{ name: string; href: string }>;
	admin?: boolean;
}

export const navigationRoutes: NavigationRoute[] = [
	{
		name: 'Home',
		href: '/',
		icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-5 w-5 shrink-0">
			<path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
		</svg>`
	},
	{
		name: 'Cloud',
		href: '/admin/cloud',
		icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-5 w-5 shrink-0">
			<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z" />
		</svg>`,
		subroutes: [
			{
				name: 'Home',
				href: '/admin/cloud/home'
			},
			{
				name: 'Tasks',
				href: '/admin/cloud/tasks'
			},
			{
				name: 'API Docs',
				href: '/admin/cloud/api-docs'
			}
		],
		admin: true
	}
];

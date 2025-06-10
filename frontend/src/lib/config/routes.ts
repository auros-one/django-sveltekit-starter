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
		icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
			<path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
		</svg>`
	},
	{
		name: 'Admin',
		href: '/admin',
		icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
			<path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
		</svg>`,
		subroutes: [
			{
				name: 'Artifacts',
				href: '/admin/artifacts'
			},
			{
				name: 'Cloud Home',
				href: '/admin/cloud/home'
			},
			{
				name: 'Cloud Jobs',
				href: '/admin/cloud/jobs'
			},
			{
				name: 'API Docs',
				href: '/admin/cloud/api-docs'
			}
		],
		admin: true
	}
];

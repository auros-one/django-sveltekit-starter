import type { PageLoad } from './$types';
export const load: PageLoad = ({ url }) => {
	return {
		key: url.searchParams.get('key')
	};
};

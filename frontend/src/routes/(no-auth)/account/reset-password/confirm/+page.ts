import type { PageLoad } from './$types';
export const load: PageLoad = ({ url }) => {
	return {
		token: url.searchParams.get('token'),
		uid: url.searchParams.get('uid')
	};
};

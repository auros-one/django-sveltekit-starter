import { clientInit } from '@jill64/sentry-sveltekit-cloudflare';
import { PUBLIC_SENTRY_DSN } from '$env/static/public';

const onError = clientInit(PUBLIC_SENTRY_DSN, {
	sentryOptions: {
		tunnel: '/sentry'
	}
});

export const handleError = onError();

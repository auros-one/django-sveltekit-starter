import * as Sentry from '@sentry/sveltekit';
import { PUBLIC_SENTRY_DSN } from '$env/static/public';

Sentry.init({
	dsn: PUBLIC_SENTRY_DSN || '',
	tracesSampleRate: 1.0,
	tunnel: '/sentry'
});

export const handleError = Sentry.handleErrorWithSentry();

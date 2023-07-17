/*
SENTRY CAN'T DO SERVER-SIDE TRACKING YET FOR EDGE COMPUTING YET
https://github.com/getsentry/sentry-javascript/issues/8291

import * as Sentry from '@sentry/sveltekit';

Sentry.init({
	dsn: process.env.PUBLIC_SENTRY_DSN || '',
	tracesSampleRate: 1.0
});

export const handleError = Sentry.handleErrorWithSentry();


// If we ever want to add our own handler, we can use SvelteKit's
// sequence function to add our handler(s) after the Sentry handler:
// export const handle = sequence(Sentry.sentryHandle(), yourHandler());
export const handle = Sentry.sentryHandle();
*/

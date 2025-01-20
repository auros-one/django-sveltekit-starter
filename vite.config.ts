import { sentryVitePlugin } from '@sentry/vite-plugin';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { SENTRY_ORG, SENTRY_PROJECT, SENTRY_AUTH_TOKEN } from '$env/static/private';
export default defineConfig({
	build: {
		sourcemap: true
	},
	plugins: [
		sentryVitePlugin({
			org: SENTRY_ORG,
			project: SENTRY_PROJECT,
			authToken: SENTRY_AUTH_TOKEN
		}),
		sveltekit()
	],
	ssr: {
		noExternal: ['@jill64/sentry-sveltekit-cloudflare']
	}
});

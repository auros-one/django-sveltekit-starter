import type { RequestHandler } from '@sveltejs/kit';
import { dev } from '$app/environment';
export const POST: RequestHandler = async ({ request }) => {
	if (dev) return new Response('Sentry is disabled in dev mode', { status: 200 });

	const envelope = await request.text();
	const pieces = envelope.split('\n', 2);
	const header = JSON.parse(pieces[0]);
	if (header['dsn']) {
		const dsn = new URL(header['dsn']);
		const projectId = dsn.pathname.replace(/^\/|\/$/g, '');
		const response = await fetch(`https://sentry.io/api/${projectId}/envelope/`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/x-sentry-envelope' },
			body: envelope
		});
		let result = '';
		try {
			result = await response.text();
		} catch (e) {
			// if there's an error, we don't care
		}
		return new Response(result, { status: response.status });
	}
	return new Response('Invalid project id or host', { status: 400 });
};

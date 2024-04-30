import { onDestroy, onMount } from 'svelte';

export const DEFAULT_TITLE = 'SvelteKit x Django Template';

export function setTitle(title: string) {
	if (typeof window === 'undefined') return;
	document.title = title;
	onMount(() => (document.title = title));
	onDestroy(() => (document.title = DEFAULT_TITLE));
}

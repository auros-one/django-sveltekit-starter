import { onDestroy, onMount } from 'svelte';

export const DEFAULT_TITLE = 'My App';

export function setTitle(title: string) {
	if (typeof window === 'undefined') return;
	document.title = title;
	onMount(() => (document.title = title));
	onDestroy(() => (document.title = DEFAULT_TITLE));
}

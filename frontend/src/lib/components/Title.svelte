<script lang="ts">
	import { DEFAULT_TITLE, setTitle } from '$lib/utils/title';
	export let title = DEFAULT_TITLE;
	setTitle(title);
</script>

<svelte:head>
	<title>{title}</title>
</svelte:head>

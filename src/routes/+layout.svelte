<script>
	import Title from '$lib/components/Title.svelte';
	import { DEFAULT_TITLE } from '$lib/utils/title';
	import '../app.css';
</script>

<Title title={DEFAULT_TITLE} />

<slot />

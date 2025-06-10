<script lang="ts">
	import { page } from '$app/stores';
	import IframeContainer from '$lib/components/layout/IframeContainer.svelte';

	$: iframeSrc = $page.url.searchParams.get('page')
		? '/api/admin' + $page.url.searchParams.get('page')
		: '/api/admin';
</script>

<IframeContainer src={iframeSrc} title="Cloud Home" />

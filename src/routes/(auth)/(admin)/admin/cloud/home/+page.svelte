<script lang="ts">
	import { page } from '$app/stores';
	import Spinner from '$lib/components/loading/Spinner.svelte';

	$: iframeSrc = $page.url.searchParams.get('page')
		? '/api/admin' + $page.url.searchParams.get('page')
		: '/api/admin';
</script>

<!-- The negative margins negate the padding of the higher-level layout container-->
<div class="relative -mx-4 -my-6 h-screen flex-row sm:-mx-6 lg:-mx-8">
	<div class="absolute z-[-10] flex h-full w-full items-center justify-center"><Spinner /></div>
	<iframe src={iframeSrc} class="h-full w-full" title="Backend management dashboard"></iframe>
</div>

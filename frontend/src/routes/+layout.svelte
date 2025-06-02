<script>
	import { browser } from '$app/environment';
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';
	import Title from '$lib/components/Title.svelte';
	import { DEFAULT_TITLE } from '$lib/utils/title';
	import '../app.css';

	const queryClient = new QueryClient({
		defaultOptions: {
			queries: {
				enabled: browser
			}
		}
	});
</script>

<Title title={DEFAULT_TITLE} />

<QueryClientProvider client={queryClient}>
	<slot />
</QueryClientProvider>

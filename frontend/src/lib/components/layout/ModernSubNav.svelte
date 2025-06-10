<script lang="ts">
	import { page } from '$app/stores';
	import type { NavigationRoute } from '$lib/config/routes';
	import { fade } from 'svelte/transition';

	export let routes: NavigationRoute[] = [];

	// Find the current active route with subroutes
	$: activeRouteWithSubroutes = routes.find((route) => {
		if (!route.subroutes) return false;
		return $page.url.pathname.startsWith(route.href + '/') || $page.url.pathname === route.href;
	});

	$: hasActiveSubroutes = !!activeRouteWithSubroutes?.subroutes;
</script>

{#if hasActiveSubroutes && activeRouteWithSubroutes && activeRouteWithSubroutes.subroutes}
	<div class="sticky top-16 z-40 -mt-8 mb-8" transition:fade={{ duration: 150 }}>
		<div class="border-b border-gray-200/80 bg-white/50 backdrop-blur-xl">
			<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
				<nav class="flex space-x-6 overflow-x-auto py-3">
					{#each activeRouteWithSubroutes.subroutes as subroute}
						{@const active =
							$page.url.pathname === subroute.href ||
							$page.url.pathname.startsWith(subroute.href + '/')}
						<a
							href={subroute.href}
							class="relative whitespace-nowrap pb-3 text-sm font-medium transition-colors {active
								? 'text-primary-600'
								: 'text-gray-500 hover:text-gray-700'}"
						>
							{subroute.name}
							{#if active}
								<span
									class="absolute inset-x-0 bottom-0 h-0.5 rounded-full bg-primary-600"
									transition:fade={{ duration: 200 }}
								></span>
							{/if}
						</a>
					{/each}
				</nav>
			</div>
		</div>
	</div>
{/if}

<script lang="ts">
	import { page } from '$app/stores';
	import type { NavigationRoute } from '$lib/config/routes';

	export let routes: NavigationRoute[] = [];

	// Find the current active route with subroutes
	$: activeRouteWithSubroutes = routes.find((route) => {
		if (!route.subroutes) return false;
		return $page.url.pathname.startsWith(route.href + '/') || $page.url.pathname === route.href;
	});

	$: hasActiveSubroutes = !!activeRouteWithSubroutes;
</script>

{#if hasActiveSubroutes && activeRouteWithSubroutes && activeRouteWithSubroutes.subroutes}
	<div class="border-b border-gray-200 bg-gray-50">
		<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
			<div class="flex space-x-8 overflow-x-auto py-3">
				{#each activeRouteWithSubroutes.subroutes as subroute}
					{@const active =
						$page.url.pathname === subroute.href ||
						$page.url.pathname.startsWith(subroute.href + '/')}
					<a
						href={subroute.href}
						class:bg-white={active}
						class:text-primary-600={active}
						class:shadow-sm={active}
						class:text-gray-600={!active}
						class:hover:text-gray-900={!active}
						class="whitespace-nowrap rounded-md px-3 py-2 text-sm font-medium transition-colors"
					>
						{subroute.name}
					</a>
				{/each}
			</div>
		</div>
	</div>
{/if}

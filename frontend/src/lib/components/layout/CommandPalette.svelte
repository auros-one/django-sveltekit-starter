<script lang="ts">
	import { fade, fly } from 'svelte/transition';
	import type { NavigationRoute } from '$lib/config/routes';
	import { goto } from '$app/navigation';
	import { logout } from '$lib/api/account/auth';

	export let open = false;
	export let routes: NavigationRoute[] = [];

	let searchQuery = '';
	let searchInput: HTMLInputElement;
	let selectedIndex = 0;

	// Action items
	const actionItems = [
		{
			name: 'Settings',
			href: '/account',
			type: 'action' as const,
			icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
			</svg>`,
			action: () => {
				open = false;
				goto('/account');
			}
		},
		{
			name: 'Sign out',
			href: '#',
			type: 'action' as const,
			icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
			</svg>`,
			action: () => {
				open = false;
				logout();
			}
		}
	];

	// All searchable items
	$: searchableItems = [
		...actionItems,
		...routes.flatMap((route) => {
			const items = [
				{
					name: route.name,
					href: route.subroutes ? route.subroutes[0].href : route.href,
					type: 'page' as const,
					icon: route.icon
				}
			];

			if (route.subroutes) {
				route.subroutes.forEach((subroute) => {
					items.push({
						name: `${route.name} › ${subroute.name}`,
						href: subroute.href,
						type: 'page' as const,
						icon: route.icon
					});
				});
			}

			return items;
		})
	];

	// Filter items based on search
	$: filteredItems = searchQuery
		? searchableItems.filter((item) => item.name.toLowerCase().includes(searchQuery.toLowerCase()))
		: searchableItems;

	// Reset when opened
	$: if (open) {
		searchQuery = '';
		selectedIndex = 0;
		setTimeout(() => searchInput?.focus(), 50);
	}

	function handleKeydown(e: KeyboardEvent) {
		switch (e.key) {
			case 'ArrowDown':
				e.preventDefault();
				selectedIndex = Math.min(selectedIndex + 1, filteredItems.length - 1);
				break;
			case 'ArrowUp':
				e.preventDefault();
				selectedIndex = Math.max(selectedIndex - 1, 0);
				break;
			case 'Enter':
				e.preventDefault();
				if (filteredItems[selectedIndex]) {
					selectItem(filteredItems[selectedIndex]);
				}
				break;
			case 'Escape':
				e.preventDefault();
				open = false;
				break;
		}
	}

	function selectItem(item: any) {
		if (item.action) {
			item.action();
		} else {
			goto(item.href);
			open = false;
		}
	}
</script>

{#if open}
	<div
		class="fixed inset-0 z-50 overflow-y-auto p-4 sm:p-6 md:p-20"
		transition:fade={{ duration: 150 }}
	>
		<!-- Backdrop -->
		<div
			class="fixed inset-0 bg-gray-500/25 backdrop-blur-sm"
			on:click={() => (open = false)}
			on:keydown={() => {}}
			role="button"
			tabindex="-1"
		/>

		<!-- Modal -->
		<div
			transition:fly={{ y: -20, duration: 200 }}
			class="relative mx-auto max-w-2xl transform rounded-xl bg-white shadow-2xl ring-1 ring-gray-900/5"
		>
			<!-- Search Input -->
			<div class="relative">
				<svg
					class="pointer-events-none absolute left-4 top-3.5 h-5 w-5 text-gray-400"
					viewBox="0 0 20 20"
					fill="currentColor"
				>
					<path
						fill-rule="evenodd"
						d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
						clip-rule="evenodd"
					/>
				</svg>
				<input
					bind:this={searchInput}
					bind:value={searchQuery}
					on:keydown={handleKeydown}
					type="text"
					class="h-12 w-full border-0 bg-transparent pl-11 pr-4 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
					placeholder="Search..."
				/>
			</div>

			<!-- Results -->
			{#if filteredItems.length > 0}
				<div class="max-h-96 scroll-py-2 overflow-y-auto border-t border-gray-100 py-2">
					{#each filteredItems as item, index}
						<button
							on:click={() => selectItem(item)}
							on:mouseenter={() => (selectedIndex = index)}
							class="flex w-full items-center gap-3 px-4 py-2 text-left text-sm {selectedIndex ===
							index
								? 'bg-primary-50 text-primary-700'
								: 'text-gray-700 hover:bg-gray-50'}"
						>
							{#if item.icon}
								<span class="h-4 w-4 flex-shrink-0 opacity-60">
									{@html item.icon}
								</span>
							{/if}
							<span class="flex-1">{item.name}</span>
							<span class="text-xs text-gray-400">
								{item.type === 'page' ? 'Page' : 'Action'}
							</span>
						</button>
					{/each}
				</div>
			{:else if searchQuery}
				<div class="border-t border-gray-100 px-6 py-14 text-center text-sm">
					<p class="text-gray-500">
						No results for "<span class="font-semibold text-gray-900">{searchQuery}</span>"
					</p>
				</div>
			{/if}

			<!-- Footer -->
			<div
				class="flex items-center justify-end gap-3 border-t border-gray-100 px-4 py-3 text-xs text-gray-500"
			>
				<div class="flex items-center gap-1">
					<kbd class="rounded bg-gray-100 px-1.5 py-0.5 font-medium">↑</kbd>
					<kbd class="rounded bg-gray-100 px-1.5 py-0.5 font-medium">↓</kbd>
					<span>Navigate</span>
				</div>
				<div class="flex items-center gap-1">
					<kbd class="rounded bg-gray-100 px-1.5 py-0.5 font-medium">↵</kbd>
					<span>Select</span>
				</div>
				<div class="flex items-center gap-1">
					<kbd class="rounded bg-gray-100 px-1.5 py-0.5 font-medium">esc</kbd>
					<span>Close</span>
				</div>
			</div>
		</div>
	</div>
{/if}

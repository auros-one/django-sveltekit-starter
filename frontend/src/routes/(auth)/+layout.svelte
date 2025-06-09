<script lang="ts">
	import { fade } from 'svelte/transition';
	import type { LayoutData } from './$types';
	import { user } from '$lib/stores/account';
	import Spinner from '$lib/components/loading/Spinner.svelte';
	import AuthProvider from '$lib/components/layout/AuthProvider.svelte';
	import HorizontalNavbar from '$lib/components/layout/HorizontalNavbar.svelte';
	import SubNavigation from '$lib/components/layout/SubNavigation.svelte';
	import { navigationRoutes } from '$lib/config/routes';

	/**
	 * This layout component now focuses purely on layout structure.
	 * Authentication logic is handled by the AuthProvider component.
	 */

	export let data: LayoutData;

	let isLoading = true;
	let showLoadingMessage = false;

	// Show loading message after 2 seconds
	setTimeout(() => {
		showLoadingMessage = true;
	}, 2000);
</script>

<AuthProvider {data} bind:isLoading>
	{#if $user && !isLoading}
		<div class="min-h-screen bg-gray-50">
			<!-- Horizontal Navigation -->
			<HorizontalNavbar routes={navigationRoutes} />

			<!-- Sub Navigation (shows when a route with subroutes is active) -->
			<SubNavigation routes={navigationRoutes} />

			<!-- Main Content -->
			<main class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
				<slot />
			</main>
		</div>
	{:else}
		<div class="flex h-screen flex-col items-center justify-center gap-6">
			<div class="relative flex flex-col items-center justify-center">
				<Spinner size={50} />
				{#if showLoadingMessage}
					<p
						in:fade={{ delay: 200, duration: 200 }}
						class="absolute bottom-0 w-max translate-y-[50px]"
					>
						Hold on, we are logging you in
					</p>
				{/if}
			</div>
		</div>
	{/if}
</AuthProvider>

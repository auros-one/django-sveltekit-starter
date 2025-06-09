<script lang="ts">
	import { fade } from 'svelte/transition';
	import type { LayoutData } from './$types';
	import { user } from '$lib/stores/account';
	import { page } from '$app/stores';
	import Spinner from '$lib/components/loading/Spinner.svelte';
	import AuthProvider from '$lib/components/layout/AuthProvider.svelte';
	import ModernNavbar from '$lib/components/layout/ModernNavbar.svelte';
	import { navigationRoutes } from '$lib/config/routes';

	/**
	 * Modern layout with clean design and smooth transitions
	 */

	export let data: LayoutData;

	let isLoading = true;
	let showLoadingMessage = false;

	// Show loading message after 2 seconds
	setTimeout(() => {
		showLoadingMessage = true;
	}, 2000);

	// Check if we're on an iframe page
	$: isIframePage = ['/admin/cloud/home', '/admin/cloud/tasks', '/admin/cloud/api-docs'].some(
		(path) => $page.url.pathname.startsWith(path)
	);
</script>

<AuthProvider {data} bind:isLoading>
	{#if $user && !isLoading}
		<div class="min-h-screen bg-gray-50">
			<!-- Modern Navigation -->
			<ModernNavbar routes={navigationRoutes} />

			<!-- Main Content with conditional padding -->
			<main class="pt-16">
				{#if !isIframePage}
					<div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
						<slot />
					</div>
				{:else}
					<slot />
				{/if}
			</main>
		</div>
	{:else}
		<!-- Modern Loading State -->
		<div class="flex min-h-screen items-center justify-center bg-gray-50">
			<div class="text-center">
				<div class="relative inline-flex">
					<Spinner size={48} />
				</div>
				{#if showLoadingMessage}
					<p in:fade={{ duration: 300 }} class="mt-4 text-sm text-gray-600">Authenticating...</p>
				{/if}
			</div>
		</div>
	{/if}
</AuthProvider>

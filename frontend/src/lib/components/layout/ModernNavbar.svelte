<script lang="ts">
	import { page } from '$app/stores';
	import { user } from '$lib/stores/account';
	import type { NavigationRoute } from '$lib/config/routes';
	import { logout } from '$lib/api/account/auth';
	import { fade, fly } from 'svelte/transition';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import CommandPalette from './CommandPalette.svelte';

	export let routes: NavigationRoute[] = [];

	let showMobileMenu = false;
	let showUserMenu = false;
	let showCommandPalette = false;
	let scrolled = false;
	let hoveredRoute = '';
	let dropdownTimeout: ReturnType<typeof setTimeout>;

	// Handle dropdown hover with delay
	function handleMouseEnter(routeName: string) {
		clearTimeout(dropdownTimeout);
		hoveredRoute = routeName;
	}

	function handleMouseLeave() {
		dropdownTimeout = setTimeout(() => {
			hoveredRoute = '';
		}, 150);
	}

	// Handle scroll for navbar appearance
	onMount(() => {
		const handleScroll = () => {
			scrolled = window.scrollY > 10;
		};
		window.addEventListener('scroll', handleScroll);
		return () => {
			window.removeEventListener('scroll', handleScroll);
			clearTimeout(dropdownTimeout);
		};
	});

	// Handle keyboard shortcuts
	function handleKeydown(e: KeyboardEvent) {
		if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
			e.preventDefault();
			showCommandPalette = !showCommandPalette;
		}
		if (e.key === 'Escape') {
			showCommandPalette = false;
			showUserMenu = false;
		}
	}

	// Get user initials
	function getUserInitials(email: string | undefined) {
		if (!email) return 'U';
		const parts = email.split('@')[0].split('.');
		if (parts.length > 1) {
			return (parts[0][0] + parts[1][0]).toUpperCase();
		}
		return email[0].toUpperCase();
	}
</script>

<svelte:window on:keydown={handleKeydown} />

<!-- Modern Floating Navbar -->
<nav
	class="fixed left-0 right-0 top-0 z-50 transition-all duration-300 {scrolled
		? 'border-b border-gray-200/50 bg-white/80 backdrop-blur-xl'
		: ''}"
>
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="flex h-16 items-center justify-between">
			<!-- Left: Logo -->
			<div class="flex items-center">
				<a href="/" class="flex items-center space-x-2.5 focus:outline-none">
					<div class="relative h-8 w-8 overflow-hidden rounded-lg shadow-sm">
						<img class="h-full w-full" src="/logo.png" alt="Logo" />
					</div>
					<span class="text-lg font-semibold text-gray-900">My App</span>
				</a>
			</div>

			<!-- Center: Navigation (Desktop) -->
			<div class="hidden md:flex md:items-center md:space-x-1">
				{#each routes.filter((route) => !route.admin || $user?.is_superuser) as route}
					{@const href = route.subroutes ? route.subroutes[0].href : route.href}
					{@const active =
						$page.url.pathname.startsWith(route.href + '/') || $page.url.pathname === route.href}

					{#if route.subroutes}
						<!-- Route with dropdown -->
						<div class="relative">
							<button
								on:click={() => goto(href)}
								on:mouseenter={() => handleMouseEnter(route.name)}
								on:mouseleave={handleMouseLeave}
								class="relative flex items-center gap-1 px-3 py-2 text-sm font-medium transition-colors {active
									? 'text-gray-900'
									: 'text-gray-600 hover:text-gray-900'}"
							>
								{#if active}
									<span
										class="absolute inset-0 rounded-md bg-gray-100"
										transition:fade={{ duration: 200 }}
									></span>
								{/if}
								<span class="relative flex items-center gap-1.5">
									{#if route.icon}
										<span class="h-4 w-4 opacity-70">{@html route.icon}</span>
									{/if}
									{route.name}
									<svg
										class="h-3 w-3 opacity-50"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M19 9l-7 7-7-7"
										/>
									</svg>
								</span>
							</button>

							<!-- Dropdown menu -->
							{#if hoveredRoute === route.name}
								<div
									class="dropdown-menu absolute left-0 top-full w-56 origin-top-left"
									on:mouseenter={() => handleMouseEnter(route.name)}
									on:mouseleave={handleMouseLeave}
									role="menu"
									tabindex="-1"
								>
									<div
										transition:fly={{ y: -5, duration: 150 }}
										class="mt-1 rounded-lg border border-gray-200 bg-white shadow-lg"
									>
										<div class="p-1">
											{#each route.subroutes as subroute}
												<a
													href={subroute.href}
													class="block rounded-md px-3 py-2 text-sm text-gray-700 transition-colors hover:bg-gray-50 {$page
														.url.pathname === subroute.href ||
													$page.url.pathname.startsWith(subroute.href + '/')
														? 'bg-gray-50 text-primary-600'
														: ''}"
												>
													{subroute.name}
												</a>
											{/each}
										</div>
									</div>
								</div>
							{/if}
						</div>
					{:else}
						<!-- Regular route -->
						<a
							{href}
							class="relative px-3 py-2 text-sm font-medium transition-colors {active
								? 'text-gray-900'
								: 'text-gray-600 hover:text-gray-900'}"
						>
							{#if active}
								<span
									class="absolute inset-0 rounded-md bg-gray-100"
									transition:fade={{ duration: 200 }}
								></span>
							{/if}
							<span class="relative flex items-center gap-1.5">
								{#if route.icon}
									<span class="h-4 w-4 opacity-70">{@html route.icon}</span>
								{/if}
								{route.name}
							</span>
						</a>
					{/if}
				{/each}
			</div>

			<!-- Right: Actions -->
			<div class="flex items-center space-x-3">
				<!-- Command Palette Trigger -->
				<button
					on:click={() => (showCommandPalette = true)}
					class="hidden items-center space-x-2 rounded-md border border-gray-200 bg-gray-50 px-3 py-1.5 text-sm text-gray-600 transition-all hover:border-gray-300 hover:bg-gray-100 md:flex"
				>
					<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
						/>
					</svg>
					<span>Search</span>
					<kbd class="rounded bg-gray-100 px-1.5 py-0.5 text-xs font-medium text-gray-500">⌘K</kbd>
				</button>

				<!-- User Menu -->
				<div class="relative">
					<button
						on:click={() => (showUserMenu = !showUserMenu)}
						class="flex items-center space-x-2 rounded-full p-1 transition-colors hover:bg-gray-100"
					>
						<div
							class="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-sm font-medium text-white shadow-sm"
						>
							{getUserInitials($user?.email)}
						</div>
					</button>

					<!-- Dropdown -->
					{#if showUserMenu}
						<div
							transition:fly={{ y: -10, duration: 200 }}
							class="absolute right-0 mt-2 w-64 origin-top-right"
						>
							<!-- Backdrop -->
							<div
								class="fixed inset-0"
								on:click={() => (showUserMenu = false)}
								on:keydown={() => {}}
								role="button"
								tabindex="-1"
							></div>

							<!-- Menu -->
							<div class="relative z-20 rounded-lg border border-gray-200 bg-white shadow-lg">
								<div class="border-b border-gray-100 p-4">
									<p class="text-sm font-medium text-gray-900">{$user?.email}</p>
									<p class="mt-0.5 text-xs text-gray-500">
										{$user?.is_superuser ? 'Administrator' : 'User'}
									</p>
								</div>
								<div class="p-1">
									<a
										href="/account"
										on:click={() => (showUserMenu = false)}
										class="flex items-center space-x-2 rounded-md px-3 py-2 text-sm text-gray-700 transition-colors hover:bg-gray-100"
									>
										<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
											/>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
											/>
										</svg>
										<span>Settings</span>
									</a>
									<button
										on:click={() => {
											showUserMenu = false;
											logout();
										}}
										class="flex w-full items-center space-x-2 rounded-md px-3 py-2 text-sm text-gray-700 transition-colors hover:bg-gray-100"
									>
										<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
											/>
										</svg>
										<span>Sign out</span>
									</button>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<!-- Mobile Menu Toggle -->
				<button
					on:click={() => (showMobileMenu = !showMobileMenu)}
					class="rounded-md p-2 text-gray-600 transition-colors hover:bg-gray-100 md:hidden"
				>
					<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						{#if showMobileMenu}
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M6 18L18 6M6 6l12 12"
							/>
						{:else}
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M4 6h16M4 12h16M4 18h16"
							/>
						{/if}
					</svg>
				</button>
			</div>
		</div>
	</div>
</nav>

<!-- Mobile Slide-out Menu -->
{#if showMobileMenu}
	<div class="fixed inset-0 z-50 md:hidden" transition:fade={{ duration: 200 }}>
		<!-- Backdrop -->
		<div
			class="fixed inset-0 bg-black/20 backdrop-blur-sm"
			on:click={() => (showMobileMenu = false)}
			on:keydown={() => {}}
			role="button"
			tabindex="-1"
		></div>

		<!-- Slide-out Panel -->
		<div
			transition:fly={{ x: 300, duration: 300 }}
			class="fixed bottom-0 right-0 top-0 w-full max-w-sm bg-white shadow-xl"
		>
			<div class="flex h-16 items-center justify-between border-b border-gray-100 px-4">
				<span class="text-lg font-semibold">Menu</span>
				<button
					on:click={() => (showMobileMenu = false)}
					class="rounded-md p-2 text-gray-600 transition-colors hover:bg-gray-100"
					aria-label="Close menu"
				>
					<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
				</button>
			</div>

			<div class="overflow-y-auto p-4">
				<!-- User Info -->
				<div class="mb-6 flex items-center space-x-3 rounded-lg bg-gray-50 p-3">
					<div
						class="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-sm font-medium text-white"
					>
						{getUserInitials($user?.email)}
					</div>
					<div class="min-w-0 flex-1">
						<p class="truncate text-sm font-medium text-gray-900">{$user?.email}</p>
						<p class="text-xs text-gray-500">
							{$user?.is_superuser ? 'Administrator' : 'User'}
						</p>
					</div>
				</div>

				<!-- Navigation -->
				<nav class="space-y-1">
					{#each routes.filter((route) => !route.admin || $user?.is_superuser) as route}
						{@const href = route.subroutes ? route.subroutes[0].href : route.href}
						{@const active =
							$page.url.pathname.startsWith(route.href + '/') || $page.url.pathname === route.href}
						<div>
							<a
								{href}
								on:click={() => !route.subroutes && (showMobileMenu = false)}
								class="flex items-center space-x-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors {active
									? 'bg-primary-50 text-primary-700'
									: 'text-gray-700 hover:bg-gray-50'}"
							>
								{#if route.icon}
									<span class="h-5 w-5">{@html route.icon}</span>
								{/if}
								<span class="flex-1">{route.name}</span>
								{#if route.subroutes}
									<svg
										class="h-4 w-4 opacity-50"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M19 9l-7 7-7-7"
										/>
									</svg>
								{/if}
							</a>

							<!-- Mobile subroutes -->
							{#if route.subroutes && active}
								<div class="ml-10 mt-1 space-y-1">
									{#each route.subroutes as subroute}
										<a
											href={subroute.href}
											on:click={() => (showMobileMenu = false)}
											class="block rounded-md px-3 py-2 text-sm text-gray-600 transition-colors hover:bg-gray-50 {$page
												.url.pathname === subroute.href ||
											$page.url.pathname.startsWith(subroute.href + '/')
												? 'bg-gray-50 text-primary-600'
												: ''}"
										>
											{subroute.name}
										</a>
									{/each}
								</div>
							{/if}
						</div>
					{/each}
				</nav>

				<!-- Actions -->
				<div class="mt-6 space-y-1 border-t border-gray-100 pt-6">
					<a
						href="/account"
						on:click={() => (showMobileMenu = false)}
						class="flex items-center space-x-3 rounded-lg px-3 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
					>
						<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
							/>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>
						<span>Settings</span>
					</a>
					<button
						on:click={() => {
							showMobileMenu = false;
							logout();
						}}
						class="flex w-full items-center space-x-3 rounded-lg px-3 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
					>
						<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
							/>
						</svg>
						<span>Sign out</span>
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}

<!-- Command Palette -->
{#if showCommandPalette}
	<CommandPalette bind:open={showCommandPalette} {routes} />
{/if}

<style>
	/* Add subtle animation to active nav item background */
	:global(.nav-active-bg) {
		animation: fadeIn 200ms ease-out;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: scale(0.95);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}
</style>

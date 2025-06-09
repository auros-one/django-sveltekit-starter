<script lang="ts">
	import { page } from '$app/stores';
	import { user } from '$lib/stores/account';
	import type { NavigationRoute } from '$lib/config/routes';
	import { logout } from '$lib/api/account/auth';

	export let routes: NavigationRoute[] = [];

	let showMobileMenu = false;
	let showUserMenu = false;
</script>

<nav class="border-b border-gray-200 bg-white shadow-sm">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="flex h-16 justify-between">
			<!-- Left side - Logo and Navigation -->
			<div class="flex">
				<!-- Logo -->
				<div class="flex flex-shrink-0 items-center">
					<img class="h-8 w-auto" src="/logo.png" alt="Your logo" />
					<span class="ml-2 text-lg font-semibold text-gray-900">My App</span>
				</div>

				<!-- Desktop Navigation -->
				<div class="hidden md:ml-6 md:flex md:items-center md:space-x-8">
					{#each routes.filter((route) => !route.admin) as route}
						{@const href = route.subroutes ? route.subroutes[0].href : route.href}
						{@const active =
							$page.url.pathname.startsWith(route.href + '/') || $page.url.pathname === route.href}
						<a
							{href}
							class:border-primary-500={active}
							class:text-gray-900={active}
							class:border-transparent={!active}
							class:text-gray-500={!active}
							class:hover:border-gray-300={!active}
							class:hover:text-gray-700={!active}
							class="inline-flex items-center gap-x-2 border-b-2 px-1 pt-1 text-sm font-medium transition-colors"
						>
							{@html route.icon}
							{route.name}
						</a>
					{/each}

					<!-- Admin section -->
					{#if $user?.is_superuser}
						{#each routes.filter((route) => route.admin) as route}
							{@const href = route.subroutes ? route.subroutes[0].href : route.href}
							{@const active =
								$page.url.pathname.startsWith(route.href + '/') ||
								$page.url.pathname === route.href}
							<div class="relative">
								<a
									{href}
									class:border-primary-500={active}
									class:text-gray-900={active}
									class:border-transparent={!active}
									class:text-gray-500={!active}
									class:hover:border-gray-300={!active}
									class:hover:text-gray-700={!active}
									class="inline-flex items-center gap-x-2 border-b-2 px-1 pt-1 text-sm font-medium transition-colors"
								>
									{@html route.icon}
									{route.name}
								</a>
							</div>
						{/each}
					{/if}
				</div>
			</div>

			<!-- Right side - User menu -->
			<div class="flex items-center">
				<!-- Desktop user menu -->
				<div class="relative hidden md:block">
					<button
						type="button"
						class="flex items-center rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
						on:click={() => (showUserMenu = !showUserMenu)}
					>
						<span class="sr-only">Open user menu</span>
						<div class="flex items-center space-x-2 px-2 py-1">
							<div class="flex h-6 w-6 items-center justify-center rounded-full bg-primary-600">
								<span class="text-xs font-medium text-white">
									{$user?.email?.charAt(0).toUpperCase() || 'U'}
								</span>
							</div>
							<span
								class="hidden max-w-[150px] truncate text-sm font-medium text-gray-700 lg:block"
							>
								{$user?.email || 'User'}
							</span>
						</div>
					</button>

					{#if showUserMenu}
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<!-- svelte-ignore a11y-no-static-element-interactions -->
						<div class="fixed inset-0 z-10" on:click={() => (showUserMenu = false)}></div>
						<div
							class="absolute right-0 z-20 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5"
						>
							<a
								href="/account"
								class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
								class:bg-gray-100={$page.url.pathname.startsWith('/account')}
								on:click={() => (showUserMenu = false)}
							>
								Account Settings
							</a>
							<button
								class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100"
								on:click={() => {
									showUserMenu = false;
									logout();
								}}
							>
								Sign out
							</button>
						</div>
					{/if}
				</div>

				<!-- Mobile menu button -->
				<button
					type="button"
					class="rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 md:hidden"
					on:click={() => (showMobileMenu = !showMobileMenu)}
				>
					<span class="sr-only">Open main menu</span>
					<svg
						class="h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
						/>
					</svg>
				</button>
			</div>
		</div>
	</div>

	<!-- Mobile menu -->
	{#if showMobileMenu}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<div
			class="fixed inset-0 z-10 bg-black bg-opacity-25 md:hidden"
			on:click={() => (showMobileMenu = false)}
		></div>
		<div class="relative z-20 border-t border-gray-200 bg-white md:hidden">
			<div class="space-y-1 px-4 pb-3 pt-2">
				{#each routes.filter((route) => !route.admin) as route}
					{@const href = route.subroutes ? route.subroutes[0].href : route.href}
					{@const active =
						$page.url.pathname.startsWith(route.href + '/') || $page.url.pathname === route.href}
					<a
						{href}
						class:bg-primary-50={active}
						class:border-primary-500={active}
						class:text-primary-700={active}
						class:border-transparent={!active}
						class:text-gray-600={!active}
						class:hover:bg-gray-50={!active}
						class:hover:border-gray-300={!active}
						class:hover:text-gray-800={!active}
						class="flex items-center gap-x-3 border-l-4 py-2 pl-3 pr-4 text-base font-medium"
						on:click={() => (showMobileMenu = false)}
					>
						{@html route.icon}
						{route.name}
					</a>
				{/each}

				{#if $user?.is_superuser}
					<div class="border-t border-gray-200 pt-4">
						<div class="px-4 pb-2">
							<p class="text-xs font-semibold uppercase tracking-wider text-gray-500">Admin</p>
						</div>
						{#each routes.filter((route) => route.admin) as route}
							{@const href = route.subroutes ? route.subroutes[0].href : route.href}
							{@const active =
								$page.url.pathname.startsWith(route.href + '/') ||
								$page.url.pathname === route.href}
							<a
								{href}
								class:bg-primary-50={active}
								class:border-primary-500={active}
								class:text-primary-700={active}
								class:border-transparent={!active}
								class:text-gray-600={!active}
								class:hover:bg-gray-50={!active}
								class:hover:border-gray-300={!active}
								class:hover:text-gray-800={!active}
								class="flex items-center gap-x-3 border-l-4 py-2 pl-3 pr-4 text-base font-medium"
								on:click={() => (showMobileMenu = false)}
							>
								{@html route.icon}
								{route.name}
							</a>
						{/each}
					</div>
				{/if}

				<!-- Mobile user section -->
				<div class="border-t border-gray-200 pt-4">
					<div class="flex items-center px-4">
						<div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary-600">
							<span class="text-sm font-medium text-white">
								{$user?.email?.charAt(0).toUpperCase() || 'U'}
							</span>
						</div>
						<div class="ml-3">
							<div class="truncate text-base font-medium text-gray-800">
								{$user?.email || 'User'}
							</div>
						</div>
					</div>
					<div class="mt-3 space-y-1">
						<a
							href="/account"
							class="block px-4 py-2 text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800"
							class:bg-gray-100={$page.url.pathname.startsWith('/account')}
							on:click={() => (showMobileMenu = false)}
						>
							Account Settings
						</a>
						<button
							class="block w-full px-4 py-2 text-left text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800"
							on:click={() => {
								showMobileMenu = false;
								logout();
							}}
						>
							Sign out
						</button>
					</div>
				</div>
			</div>
		</div>
	{/if}
</nav>

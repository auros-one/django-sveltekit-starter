<script lang="ts">
	import { getUser } from '$lib/api/account/user';
	import { onMount, onDestroy } from 'svelte';
	import { user } from '$lib/stores/account';
	import { jwt } from '$lib/stores/auth';
	import Spinner from '$lib/components/loading/Spinner.svelte';
	import { goto } from '$app/navigation';
	import { refresh } from '$lib/api/account/auth';
	import { fade } from 'svelte/transition';
	import type { LayoutData } from './$types';
	import { page } from '$app/stores';

	/**
	 * This is a layout component that is used to wrap all authenticated routes.
	 *
	 * The 'onMount' of this component starts the JWT refresh loop, which will
	 * refresh the JWT token when it is about to expire. If anything goes wrong
	 * during the refresh loop, the user is redirected to the login page.
	 */

	export let data: LayoutData;
	$user = data.user;

	let refreshTokenLoop: number | undefined = undefined;

	async function initJWTRefreshLoop() {
		const result = await refresh();
		$jwt = result.token;

		const expirationDate = new Date(result.expiration);
		const refreshRateMS = expirationDate.valueOf() - Date.now() - 5000;

		refreshTokenLoop = setInterval(async () => {
			try {
				const updatedTokenInfo = await refresh();
				$jwt = updatedTokenInfo.token;
			} catch {
				goto('/account/login');
				clearInterval(refreshTokenLoop); // Clear the interval if an error occurs
			}
		}, refreshRateMS);
	}

	let showLoadingMessage = false;

	onMount(async () => {
		try {
			setTimeout(() => {
				showLoadingMessage = true;
			}, 2000);
			await initJWTRefreshLoop();
			getUser();
		} catch {
			goto('/account/login');
		}
	});

	onDestroy(() => {
		// Clear the interval when the component is destroyed
		if (typeof refreshTokenLoop === 'number') clearInterval(refreshTokenLoop);
	});

	let routes = [
		{
			name: 'Home',
			href: '/',
			icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6 shrink-0">
				<path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
			</svg>`
		},
		{
			name: 'Cloud',
			href: '/admin/cloud',
			icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6 shrink-0">
				<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z" />
			</svg>`,
			subroutes: [
				{
					name: 'Home',
					href: '/admin/cloud/home'
				},
				{
					name: 'API Docs',
					href: '/admin/cloud/api-docs'
				}
			],
			admin: true
		}
	];
</script>

{#if $user}
	<div class="relative flex min-h-screen flex-col">
		<div class="flex h-screen overflow-hidden">
			<!-- Vertical Navigation Bar -->
			<div
				class="flex w-[220px] flex-none flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6"
			>
				<!-- Logo -->
				<div class="flex h-16 shrink-0 items-center">
					<div class="size-8">
						<img class="h-8 w-auto" src="/logo.png" alt="Your logo" />
					</div>
					<span class="ml-2 text-lg font-semibold text-gray-900">Your App</span>
				</div>

				<!-- Navigation -->
				<nav class="flex flex-1 flex-col">
					<ul role="list" class="-mx-2 space-y-1">
						{#each routes.filter((route) => !route.admin) as route}
							{@const href = route.subroutes ? route.subroutes[0].href : route.href}
							{@const active =
								$page.url.pathname.startsWith(route.href + '/') ||
								$page.url.pathname === route.href}
							<li>
								<a
									{href}
									class:bg-gray-100={active}
									class:text-primary-600={active}
									class:hover:bg-gray-50={!active}
									class:hover:text-primary-600={!active}
									class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6 text-gray-700"
								>
									{@html route.icon}
									{route.name}
								</a>
							</li>
						{/each}

						{#if $user.is_superuser}
							<li class="pt-5">
								<h3 class="px-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
									Admin
								</h3>
							</li>

							{#each routes.filter((route) => route.admin) as route}
								{@const href = route.subroutes ? route.subroutes[0].href : route.href}
								{@const active =
									$page.url.pathname.startsWith(route.href + '/') ||
									$page.url.pathname === route.href}
								{@const hasActiveSubroute =
									route.subroutes &&
									route.subroutes.some(
										(subroute) =>
											$page.url.pathname.startsWith(subroute.href + '/') ||
											$page.url.pathname === subroute.href
									)}
								<li>
									<a
										{href}
										class:bg-gray-100={active && !hasActiveSubroute}
										class:text-primary-600={active && !hasActiveSubroute}
										class:hover:bg-gray-50={!active || hasActiveSubroute}
										class:hover:text-primary-600={!active || hasActiveSubroute}
										class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6 text-gray-700"
									>
										{@html route.icon}
										{route.name}
									</a>
									{#if (active || hasActiveSubroute) && route.subroutes}
										<ul class="mt-1 space-y-1">
											{#each route.subroutes as subroute, index}
												{@const subActive =
													$page.url.pathname === subroute.href ||
													$page.url.pathname.startsWith(subroute.href + '/')}
												{@const isLast = index === route.subroutes.length - 1}
												<li class="relative">
													<a
														href={subroute.href}
														class:bg-gray-100={subActive}
														class:text-primary-600={subActive}
														class:hover:bg-gray-50={!subActive}
														class:hover:text-primary-600={!subActive}
														class="flex items-center rounded-md py-2 pl-9 pr-2 text-sm font-medium text-gray-600"
													>
														<span
															class={`absolute left-[18px] top-0 w-[2px] bg-gray-200 ${
																isLast ? 'h-1/2' : 'h-full'
															}`}
														></span>
														<span class="absolute left-[18px] top-1/2 h-[2px] w-[10px] bg-gray-200"
														></span>
														{subroute.name}
													</a>
												</li>
											{/each}
										</ul>
									{/if}
								</li>
							{/each}
						{/if}
					</ul>
				</nav>

				<!-- User Profile Section -->
				<div class="mt-auto pb-4">
					<a
						href="/account"
						class="group flex items-center gap-x-3 rounded-md p-2 text-sm font-semibold leading-6 text-gray-700 hover:bg-gray-50 hover:text-primary-600"
						class:bg-gray-100={$page.url.pathname.startsWith('/account')}
						class:text-primary-600={$page.url.pathname.startsWith('/account')}
					>
						<svg
							class="h-6 w-6 shrink-0 text-gray-400 group-hover:text-primary-600"
							class:text-primary-600={$page.url.pathname.startsWith('/account')}
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>
						<span class="truncate" title={$user.email}>{$user.email}</span>
					</a>
				</div>
			</div>

			<!-- Main Content -->
			<main class="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
				<slot />
			</main>
		</div>
	</div>
{:else}
	<div class="flex h-[95%] flex-col items-center justify-center gap-6">
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

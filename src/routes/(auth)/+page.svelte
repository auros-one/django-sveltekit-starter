<script>
	import { user } from '$lib/stores/account';
</script>

<div class="flex h-full flex-col items-center justify-center gap-4">
	<a href="/welcome"><img class="mx-auto h-10 w-auto" src="/favicon.png" alt="Company logo" /></a>
	<h1 class="my-4 text-2xl font-bold">Homepage</h1>

	<div class="flex flex-row gap-2">
		<a
			href="/account"
			class="flex w-full items-center rounded-md bg-primary-600 py-1 pl-1 pr-5 text-white hover:bg-primary-500"
			style="cursor:pointer;"
		>
			<div class="flex h-9 w-9 items-center justify-center rounded-full p-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="h-6 w-6"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
					/>
				</svg>
			</div>
			<p class="ml-2 overflow-hidden text-ellipsis text-white">
				{$user?.email || 'Account'}
			</p>
		</a>
	</div>
</div>

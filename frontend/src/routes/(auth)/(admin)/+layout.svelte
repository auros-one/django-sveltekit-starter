<script lang="ts">
	import { user } from '$lib/stores/account';
</script>

{#if $user.is_superuser}
	<slot />
{:else}
	<div class="w-full rounded-lg bg-white px-6 py-4">
		<div class="flex flex-row items-center gap-2">
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
					d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z"
				/>
			</svg>
			<h3 class="mb-[3px] text-lg font-semibold leading-7 text-gray-900">Admin Only Page</h3>
		</div>
		<p class="mb">
			This page is only accessible to administrators. If you believe you should have access, please
			contact support.
		</p>
	</div>
{/if}

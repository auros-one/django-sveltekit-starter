<script lang="ts">
	import type { Artifact } from '$lib/types/artifact';

	export let artifact: Artifact;
	export let onCopy: (_filename: string) => void;
	export let isCopying: boolean = false;
</script>

<div
	class="h-full rounded-lg border border-gray-200 bg-white shadow-sm transition-shadow hover:shadow-md"
>
	<div class="flex h-full flex-col p-6">
		<!-- Header -->
		<div class="flex items-start justify-between">
			<h3 class="text-lg font-semibold text-gray-900">{artifact.name}</h3>
			<span
				class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium {artifact.complexity ===
				'beginner'
					? 'bg-green-100 text-green-800'
					: artifact.complexity === 'intermediate'
						? 'bg-yellow-100 text-yellow-800'
						: 'bg-red-100 text-red-800'}"
			>
				{artifact.complexity}
			</span>
		</div>

		<!-- Category -->
		<div class="mt-1">
			<span class="text-sm text-gray-500">{artifact.category}</span>
		</div>

		<!-- Description -->
		<p class="mt-3 line-clamp-3 flex-grow text-sm text-gray-600">
			{artifact.description}
		</p>

		<!-- Tags -->
		<div class="mt-4 flex flex-wrap gap-1">
			{#each artifact.tags as tag}
				<span
					class="inline-flex items-center rounded bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700"
				>
					{tag}
				</span>
			{/each}
		</div>

		<!-- Copy Button -->
		<div class="mt-6">
			<button
				on:click={() => onCopy(artifact.filename)}
				disabled={isCopying}
				class="inline-flex w-full items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700 disabled:bg-indigo-400"
			>
				{#if isCopying}
					<svg
						class="-ml-1 mr-2 h-4 w-4 animate-spin text-white"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
					>
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"
						></circle>
						<path
							class="opacity-75"
							fill="currentColor"
							d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
						></path>
					</svg>
					Copied!
				{:else}
					<svg
						class="mr-2 h-4 w-4"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184"
						/>
					</svg>
					Copy Artifact Prompt
				{/if}
			</button>
		</div>
	</div>
</div>

<style>
	.line-clamp-3 {
		display: -webkit-box;
		-webkit-line-clamp: 3;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>

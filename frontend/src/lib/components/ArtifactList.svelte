<script lang="ts">
	import ArtifactCard from './ArtifactCard.svelte';
	import type { Artifact } from '$lib/types/artifact';

	export let artifacts: Artifact[] = [];
	export let copyingStates: Record<string, boolean> = {};
	export let onCopy: (_filename: string) => void;
</script>

<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
	{#each artifacts as artifact}
		<ArtifactCard {artifact} {onCopy} isCopying={copyingStates[artifact.filename]} />
	{/each}
</div>

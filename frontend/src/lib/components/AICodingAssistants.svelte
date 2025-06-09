<script lang="ts">
	interface AIAssistant {
		name: string;
		logoPath: string;
	}

	const aiAssistants: AIAssistant[] = [
		{ name: 'Claude', logoPath: '/landing-page/claude.png' },
		{ name: 'OpenAI', logoPath: '/landing-page/openai.png' },
		{ name: 'Devin', logoPath: '/landing-page/devin.png' },
		{ name: 'Cursor', logoPath: '/landing-page/cursor.png' }
	];
</script>

<div class="flex flex-wrap items-center justify-center gap-6">
	{#each aiAssistants as assistant}
		<div class="text-center">
			<div
				class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm"
			>
				<img
					src={assistant.logoPath}
					alt={assistant.name}
					class="h-full w-full object-contain p-2"
				/>
			</div>
			<p class="mt-2 text-sm font-medium text-gray-700">{assistant.name}</p>
		</div>
	{/each}
</div>

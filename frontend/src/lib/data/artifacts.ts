import type { Artifact } from '$lib/types/artifact';

export const artifacts: Artifact[] = [
	{
		name: 'ChatUI Artifact System',
		description:
			'A production-ready, frontend-first streaming chat interface with extensible artifact support. Build sophisticated chat interfaces with real-time token streaming and rich content rendering.',
		filename: 'chatui-artifact.md',
		category: 'UI Components',
		complexity: 'advanced',
		tags: ['chat', 'streaming', 'real-time', 'typescript', 'react']
	},
	{
		name: 'Basic Data Table',
		description:
			'A simple, reusable data table component with sorting, pagination, and responsive design. Perfect for displaying structured data with TypeScript type safety.',
		filename: 'basic-table-artifact.md',
		category: 'UI Components',
		complexity: 'beginner',
		tags: ['table', 'data', 'sorting', 'pagination', 'typescript']
	}
	// More artifacts will be added here
];

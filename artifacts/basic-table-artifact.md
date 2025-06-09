# Basic Data Table

**Version:** 1.0.0
**Category:** UI Components
**Complexity:** beginner

## Overview

A simple, reusable data table component with sorting, pagination, and responsive design. Perfect for displaying structured data with TypeScript type safety.

## Requirements

- SvelteKit project
- TailwindCSS (already included in the template)
- No additional dependencies needed

## Implementation Guide

### 1. Create the DataTable Component

Create a new file at `frontend/src/lib/components/DataTable.svelte`:

```svelte
<script lang="ts" generics="T extends Record<string, any>">
	export let data: T[] = [];
	export let columns: Array<{
		key: keyof T;
		label: string;
		sortable?: boolean;
		formatter?: (value: any) => string;
	}> = [];
	export let pageSize = 10;

	let currentPage = 1;
	let sortKey: keyof T | null = null;
	let sortDirection: 'asc' | 'desc' = 'asc';

	$: sortedData = sortData(data, sortKey, sortDirection);
	$: paginatedData = paginate(sortedData, currentPage, pageSize);
	$: totalPages = Math.ceil(data.length / pageSize);

	function sortData(items: T[], key: keyof T | null, direction: 'asc' | 'desc'): T[] {
		if (!key) return items;

		return [...items].sort((a, b) => {
			const aVal = a[key];
			const bVal = b[key];

			if (aVal < bVal) return direction === 'asc' ? -1 : 1;
			if (aVal > bVal) return direction === 'asc' ? 1 : -1;
			return 0;
		});
	}

	function paginate(items: T[], page: number, size: number): T[] {
		const start = (page - 1) * size;
		return items.slice(start, start + size);
	}

	function handleSort(key: keyof T) {
		if (sortKey === key) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDirection = 'asc';
		}
	}

	function getCellValue(item: T, column: typeof columns[0]): string {
		const value = item[column.key];
		return column.formatter ? column.formatter(value) : String(value ?? '');
	}
</script>

<div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
	<table class="min-w-full divide-y divide-gray-300">
		<thead class="bg-gray-50">
			<tr>
				{#each columns as column}
					<th
						class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider {column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''}"
						on:click={() => column.sortable && handleSort(column.key)}
					>
						<div class="flex items-center gap-1">
							{column.label}
							{#if column.sortable}
								<svg
									class="w-4 h-4 {sortKey === column.key ? 'text-gray-900' : 'text-gray-400'}"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									{#if sortKey === column.key && sortDirection === 'asc'}
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12" />
									{:else if sortKey === column.key && sortDirection === 'desc'}
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 13l-5 5m0 0l-5-5m5 5V6" />
									{:else}
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
									{/if}
								</svg>
							{/if}
						</div>
					</th>
				{/each}
			</tr>
		</thead>
		<tbody class="bg-white divide-y divide-gray-200">
			{#if paginatedData.length === 0}
				<tr>
					<td colspan={columns.length} class="px-6 py-4 text-center text-gray-500">
						No data available
					</td>
				</tr>
			{:else}
				{#each paginatedData as item}
					<tr class="hover:bg-gray-50">
						{#each columns as column}
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
								{getCellValue(item, column)}
							</td>
						{/each}
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>

	{#if totalPages > 1}
		<div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
			<div class="flex-1 flex justify-between sm:hidden">
				<button
					on:click={() => currentPage = Math.max(1, currentPage - 1)}
					disabled={currentPage === 1}
					class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
				>
					Previous
				</button>
				<button
					on:click={() => currentPage = Math.min(totalPages, currentPage + 1)}
					disabled={currentPage === totalPages}
					class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
				>
					Next
				</button>
			</div>
			<div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
				<div>
					<p class="text-sm text-gray-700">
						Showing
						<span class="font-medium">{(currentPage - 1) * pageSize + 1}</span>
						to
						<span class="font-medium">{Math.min(currentPage * pageSize, data.length)}</span>
						of
						<span class="font-medium">{data.length}</span>
						results
					</p>
				</div>
				<div>
					<nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
						<button
							on:click={() => currentPage = Math.max(1, currentPage - 1)}
							disabled={currentPage === 1}
							class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
						>
							<svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
								<path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
							</svg>
						</button>
						<button
							on:click={() => currentPage = Math.min(totalPages, currentPage + 1)}
							disabled={currentPage === totalPages}
							class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
						>
							<svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
								<path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
							</svg>
						</button>
					</nav>
				</div>
			</div>
		</div>
	{/if}
</div>
```

### 2. Usage Example

Create a page or component that uses the DataTable:

```svelte
<script lang="ts">
	import DataTable from '$lib/components/DataTable.svelte';

	interface User {
		id: number;
		name: string;
		email: string;
		role: string;
		createdAt: Date;
	}

	const users: User[] = [
		{ id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin', createdAt: new Date('2024-01-15') },
		{ id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User', createdAt: new Date('2024-01-16') },
		// Add more data as needed
	];

	const columns = [
		{ key: 'id' as const, label: 'ID', sortable: true },
		{ key: 'name' as const, label: 'Name', sortable: true },
		{ key: 'email' as const, label: 'Email', sortable: true },
		{ key: 'role' as const, label: 'Role', sortable: true },
		{
			key: 'createdAt' as const,
			label: 'Created At',
			sortable: true,
			formatter: (value: Date) => value.toLocaleDateString()
		}
	];
</script>

<div class="p-4">
	<h1 class="text-2xl font-bold mb-4">Users</h1>
	<DataTable {data} {columns} pageSize={5} />
</div>
```

## Features

- **Type-safe**: Full TypeScript support with generics
- **Sortable columns**: Click column headers to sort
- **Pagination**: Navigate through large datasets
- **Responsive**: Works on mobile and desktop
- **Customizable**: Easy to style and extend
- **Formatters**: Transform data for display

## Customization Options

- Adjust `pageSize` to control items per page
- Add custom formatters for complex data types
- Style with TailwindCSS classes
- Add row actions or selection functionality
- Implement server-side pagination for large datasets

## Best Practices

1. Use meaningful column keys that match your data structure
2. Provide formatters for dates, numbers, and complex types
3. Consider server-side sorting/pagination for large datasets
4. Add loading states for async data
5. Implement proper accessibility attributes

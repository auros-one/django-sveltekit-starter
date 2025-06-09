<script lang="ts">
	import { page } from '$app/stores';

	// Check if we're on a cloud page that uses an iframe
	$: isIframePage = ['/admin/cloud/home', '/admin/cloud/tasks', '/admin/cloud/api-docs'].some(
		(path) => $page.url.pathname.startsWith(path)
	);
</script>

<!-- Remove padding for iframe pages -->
<div class={isIframePage ? '' : 'cloud-content'}>
	<slot />
</div>

<style>
	.cloud-content {
		/* Keep normal padding for non-iframe cloud pages */
		padding: 2rem 0;
	}
</style>

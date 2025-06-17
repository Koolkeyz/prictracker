<script lang="ts">
    import type { PageData } from './$types';

    let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>User Management - PriceTracker</title>
	<meta name="description" content="Manage users on the PriceTracker platform" />
</svelte:head>
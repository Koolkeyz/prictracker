<script lang="ts">
    import type { PageData } from './$types';

    let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Platform Configuration - PriceTracker</title>
	<meta name="description" content="Manage products you are tracking" />
</svelte:head>
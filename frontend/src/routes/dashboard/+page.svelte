<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<header class="container mx-auto flex flex-row items-center justify-between">
	<h1 class="text-info text-3xl font-medium self-start">Tracked Products</h1>

	<a href="/dashboard/products/add" class="btn btn-md btn-soft btn-outline btn-link rounded-lg"
		>Add Product</a
	>
</header>

<script lang="ts">
	import type { PageData } from './$types';
	import { Heading, Hr, Button, Card } from 'flowbite-svelte';
	import { PlusOutline } from 'flowbite-svelte-icons';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Dashboard - PriceTracker</title>
	<meta name="description" content="Dashboard for PriceTracker" />
</svelte:head>

<section class="items-center-safe flex flex-row justify-between">
	<Heading tag="h2">Tracked Products</Heading>
	<Button href="/dashboard/products/add" pill size="sm" class="mt-1.5">
		<PlusOutline class="me-1 size-5" />
		Add Product
	</Button>
</section>
<Hr />

<section class="">
	<Card class="bg-red-500 text-white">
		<Heading tag="h3" class="text-lg font-semibold">Important Notice</Heading>
		<p class="text-sm">
			The PriceTracker service is currently in beta. Please report any issues you encounter.
		</p>
	</Card>
</section>

<script lang="ts">
	import Icon from '$components/ui/Icon.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const addProductForm = $state({
		website: undefined as string | undefined,
		productLink: undefined as string | undefined,
		amazonASIN: undefined as string | undefined
	});

	const addProductSubmit = async (e: SubmitEvent) => {
		e.preventDefault();
		console.log('Form submitted:', addProductForm);
	};

	const validateAmazonASIN = (e: MouseEvent) => {
		e.preventDefault();
		console.log('Validating ASIN:', addProductForm.amazonASIN);
		// Basic validation for ASIN format (10 alphanumeric characters)
		const result =  /^[A-Z0-9]{10}$/.test(addProductForm.amazonASIN || '');
	};

	$effect(() => {
		if (addProductForm.website === 'amazon' && addProductForm.amazonASIN) {
			addProductForm.productLink = `https://www.amazon.com/dp/${addProductForm.amazonASIN}`;
		}
	});
</script>

<section class="container mx-auto">
	<header class="">
		<h1 class="text-info text-2xl font-semibold">Add a new Product to Track</h1>
	</header>

	<form onsubmit={addProductSubmit} class="space-y-2">
		<fieldset class="fieldset text-sm">
			<legend class="fieldset-legend ml-1.5">Website</legend>
			<select class="select" bind:value={addProductForm.website}>
				<option disabled>Pick the website you're shopping on</option>
				<option value={'amazon' as const} selected>Amazon</option>
				<option value={'newegg' as const}>NewEgg</option>
				<option value={'ebay' as const}>Ebay</option>
			</select>
		</fieldset>

		{#if addProductForm.website === 'amazon'}
			<fieldset class="fieldset text-sm">
				<legend class="fieldset-legend ml-1.5">ASIN Number</legend>
				<div class="join">
					<input
						type="text"
						class="input join-item"
						placeholder="Enter ASIN Here"
						bind:value={addProductForm.amazonASIN}
					/>
					<button class="btn join-item" type="button" onclick={validateAmazonASIN}>save</button>
				</div>
				<p class="label text-secondary">
					<Icon name={'mdi--info-circle'} class="size-4.5" />
					Product URL:
					<a
						class={'link link-secondary ml-1.5'}
						href={addProductForm.productLink}
						target="_blank"
						rel="noopener noreferrer"
					>
						https://www.amazon.com/dp/{addProductForm.amazonASIN}
					</a>
				</p>
			</fieldset>
		{/if}

		<button type="submit" class="btn btn-block my-4 rounded-lg">Submit</button>
	</form>
</section>

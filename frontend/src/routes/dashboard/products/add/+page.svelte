<script lang="ts" module>
	import { z } from 'zod';
	import { ProductSchema } from '$lib/schemas/products.schema';

	interface Step1Response {
		message: string;
		product_url: string;
		product_data: {
			product_title: string;
			product_image: string;
			product_price: number;
			product_coupon: {
				value: number;
				discount_type: 'percent' | 'fixed';
			} | null;
			product_seller: {
				ships_from: string;
				sold_by: string;
			};
		};
	}

	async function step1Validate(
		body: { productUrl: string },
		website: string
	): Promise<Step1Response> {
		const response = await fetch(`/api/products/validate/${website}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Accept: 'application/json'
			},
			body: JSON.stringify(body),
			credentials: 'include'
		});

		if (!response.ok) {
			throw new Error('Failed to validate product');
		}

		return response.json();
	}
</script>

<script lang="ts">
	import Icon from '$components/Icon.svelte';
	import type { PageData } from './$types';
	import {
		Select,
		Stepper,
		Input,
		Label,
		Heading,
		Helper,
		A,
		Span,
		Img,
		Button,
		Toast,
		P
	} from 'flowbite-svelte';
	import type { Step, SelectOptionType } from 'flowbite-svelte';
	import { InfoCircleSolid, DollarOutline } from 'flowbite-svelte-icons';

	let { data }: { data: PageData } = $props();

	// Event and state management variables
	let currentStep = $state(2);
	let isProcessingStep = $state(false);
	let shouldDisableStep1 = $state(false);
	let shouldDisableStep2 = $state(false);
	let shouldDisableStep3 = $state(false);

	// Stepper state
	let addProductSteps = $state<Step[]>([
		{
			label: 'Add',
			description: 'Product',
			status: 'completed',
			id: 1
		},
		{
			label: 'Confirm',
			description: 'Details',
			status: 'current',
			id: 2
		},
		{
			label: 'Setup',
			description: 'Scheduling',
			status: 'pending',
			id: 3
		},
		{
			label: 'Complete',
			status: 'pending',
			id: 4
		}
	]);

	// Options for the website selection dropdown
	const websiteOptions: SelectOptionType<string>[] = $state([
		{ value: 'amazon', name: 'Amazon' },
		{ value: 'newegg', name: 'Newegg' },
		{ value: 'ebay', name: 'Ebay' }
	]);

	// Form state for validation and product details
	let validationForm = $state({
		website: undefined as string | undefined,
		productId: undefined as string | undefined, // This is the Amazon product ASIN or Newegg Item Number
		productLink: undefined as string | undefined
	});

	// Form state for adding product details to backend
	let addProductForm = $state({
		userId: data.authUser._id as string,
		productPlatform: 'amazon' as string | undefined,
		productUrl: 'https://www.amazon.com/dp/B0BHJJ9Y77' as string | undefined,
		productName:
			'Samsung 990 PRO SSD NVMe M.2 PCIe Gen4, M.2 2280 Internal Solid State Hard Drive, Seq. Read Speeds Up to 7,450 MB/s for High End Computing, Gaming, and Heavy Duty Workstations, MZ-V9P2T0B/AM' as
				| undefined
				| string,
		productImage:
			'https://m.media-amazon.com/images/I/71OWtcxKgvL.__AC_SY300_SX300_QL70_FMwebp_.jpg' as
				| undefined
				| string,
		productPrice: 149.99 as undefined | number,
		productCoupon: { value: 20, discount_type: 'percent' } as
			| { value: number; discount_type: 'percent' | 'fixed' }
			| null
			| undefined,
		productSeller: { ships_from: 'Amazon.com', sold_by: 'Amazon.com' } as
			| { ships_from: string; sold_by: string }
			| null
			| undefined,
		desiredPrice: undefined as number | undefined
	});

	// Form state for adding product schedule
	let addProductScheduleForm = $state({});

	// Effect for disabling the steps submit button based on validation form
	$effect(() => {
		// Disable Step 1 button if website and productId is not set
		if (validationForm.website && validationForm.productId) shouldDisableStep1 = false;
		else shouldDisableStep1 = true;

		// Disable Step 2 button if product details are not set and desired price is not set
		if (
			addProductForm.productName &&
			addProductForm.productPrice &&
			addProductForm.desiredPrice !== undefined
		) {
			shouldDisableStep2 = false;
		} else {
			shouldDisableStep2 = true;
		}
	});

	// Form Submission handlers for product validation
	const handleStep1Submit = async (e: SubmitEvent) => {
		e.preventDefault();
		try {
			isProcessingStep = true;
			const productUrl = validationForm.productLink?.trim();
			if (!productUrl) return;
			const website = validationForm.website;
			if (!website) return;

			const response = await step1Validate({ productUrl }, website);

			addProductForm.productPlatform = website;
			addProductForm.productUrl = productUrl;
			addProductForm.productName = response.product_data.product_title;
			addProductForm.productImage = response.product_data.product_image;
			addProductForm.productPrice = response.product_data.product_price;
			addProductForm.productCoupon = response.product_data.product_coupon;
			addProductForm.productSeller = response.product_data.product_seller;

			// Update the stepper status
			addProductSteps[0].status = 'completed';
			addProductSteps[1].status = 'current';

			currentStep = 2;
		} catch (err) {
			console.error('Error in Step 1 submission:', err);
			// Show an error toast or message
			validationForm.productId = undefined; // Reset product ID on error
			validationForm.productLink = undefined; // Reset product link on error
		} finally {
			isProcessingStep = false;
		}
	};

	// Form Submission handlers for product confirmation
	const handleStep2Submit = (e: SubmitEvent) => {
		e.preventDefault();
		try {
			isProcessingStep = true;
			// Update the stepper status
			addProductSteps[1].status = 'completed';
			addProductSteps[2].status = 'current';
			currentStep = 3;
		} catch (err) {
			console.error('Error in Step 2 submission:', err);
			// Show an error toast or message
			return;
		} finally {
			isProcessingStep = false;
		}
	};

	// Form Submission handlers for Schedule setup
	const handleStep3Submit = (e: SubmitEvent) => {
		e.preventDefault();
		console.log('Step 3 Form submitted');
		// Update the stepper status
		addProductSteps[2].status = 'completed';
		addProductSteps[3].status = 'current';
	};

	// Form Submission handlers for final Confirmation and Backend submission
	const handleStep4Submit = (e: SubmitEvent) => {
		e.preventDefault();
		console.log('Step 4 Form submitted');
		// Update the stepper status
		addProductSteps[3].status = 'completed';
		currentStep = 1; // Reset to first step or navigate to another page
	};
</script>

<section class="mx-auto w-full">
	<Stepper
		steps={addProductSteps}
		classes={{
			stepper: 'mx-auto md:ps-40 mb-6'
		}}
	/>

	{#if isProcessingStep}
		<div class="relative top-20 flex w-full items-center justify-center">
			<Icon
				name="svg-spinners--blocks-shuffle-3"
				class="text-primary-700 size-80 place-self-center"
			/>
		</div>
	{:else if currentStep === 1}
		<form class="container mx-auto" onsubmit={handleStep1Submit}>
			<div class="mx-2 md:mx-8">
				<Heading tag="h3" class="">Setup Product</Heading>
				<section class="flex flex-col justify-between gap-4 md:flex-row md:items-center">
					<div class="self-start">
						<Label for="website" class="flex flex-col gap-0.5">
							Choose the website where you want to track a product
							<Select items={websiteOptions} clearable bind:value={validationForm.website} />
						</Label>

						{#if validationForm.website}
							{@const productIdLabel =
								validationForm.website === 'amazon'
									? 'Amazon ASIN number'
									: validationForm.website === 'newegg'
										? 'Newegg Item Number'
										: validationForm.website === 'ebay'
											? 'Ebay Item Number'
											: undefined}
							<Label for="productId" class="flex flex-col gap-0.5">
								Enter the {productIdLabel}
								<Input
									type="text"
									id="productId"
									placeholder={productIdLabel}
									bind:value={validationForm.productId}
									oninput={() => {
										if (validationForm.website === 'amazon')
											validationForm.productLink =
												`https://www.amazon.com/dp/${validationForm.productId}`.trim();
										else if (validationForm.website === 'newegg')
											validationForm.productLink =
												`https://www.newegg.com/p/${validationForm.productId}`.trim();
										else if (validationForm.website === 'ebay')
											validationForm.productLink =
												`https://www.ebay.com/itm/${validationForm.productId}`.trim();
										else validationForm.productLink = undefined;
									}}
								/>
								<Helper class="my-1.5">
									<Span class="flex items-center gap-1">
										<InfoCircleSolid />
										Product Link: <A href={validationForm.productLink} target="_blank"
											>{validationForm.website === 'amazon'
												? `https://www.amazon.com/dp/${validationForm.productId ?? ''}`
												: validationForm.website === 'newegg'
													? `https://www.newegg.com/p/${validationForm.productId ?? ''}`
													: `https://www.ebay.com/itm/${validationForm.productId ?? ''}`}</A
										></Span
									>
								</Helper>
							</Label>
						{/if}
					</div>
					{#if validationForm.website}
						<Img
							src={validationForm.website == 'amazon'
								? '/amazon-asin-number.png'
								: validationForm.website == 'newegg'
									? '/newegg-item-number.png'
									: validationForm.website == 'ebay'
										? '/ebay-item-number.png'
										: undefined}
							alt="Product ID Example"
							class="max-w-xs rounded-lg md:max-w-2xl"
						/>
					{/if}
				</section>
				<Button type="submit" class="my-4 w-full" pill disabled={shouldDisableStep1}
					>Validate Product</Button
				>
			</div>
		</form>
	{:else if currentStep === 2}
		<form class="container mx-auto" onsubmit={handleStep2Submit}>
			<div class="mx-2 md:mx-8">
				<Heading tag="h3" class="mb-2"><Span highlight="orange">Product Details</Span></Heading>
				<section class="flex flex-col-reverse justify-between gap-4 md:flex-row md:items-center">
					<div class="w-full self-start">
						<Heading tag="h4" class="max-w-2xl">
							{addProductForm.productName ?? 'Product Name Not Available'}
						</Heading>

						<Heading tag="h4" class="my-2 max-w-2xl">
							<Span class="text-secondary-500">
								${addProductForm.productPrice?.toFixed(2) ?? 'N/A'}
							</Span>

							{#if addProductForm.productCoupon}
								<Span class="text-lg" italic
									>{addProductForm.productCoupon.discount_type === 'fixed'
										? '$'
										: ''}{addProductForm.productCoupon.value}
									{addProductForm.productCoupon.discount_type === 'percent' ? '%' : ''}
									coupon available
								</Span>
							{/if}
						</Heading>

						<P>
							Shipped from
							<Span italic highlight="blue">{addProductForm.productSeller?.ships_from}</Span>
							& Sold by
							<Span italic highlight="blue">{addProductForm.productSeller?.sold_by}</Span>.
						</P>
						<Label for="desiredPrice" class="mt-4 flex flex-col gap-1">
							Enter your desired price to track this product
							<Input
								type="number"
								id="desiredPrice"
								placeholder="Desired Price"
								bind:value={addProductForm.desiredPrice}
								min="0"
								step="0.01"
								class="w-full max-w-md ps-8"
								oninput={() => {
									// Ensure the desired price decimals are limited to two decimal places
									if (addProductForm.desiredPrice !== undefined) {
										addProductForm.desiredPrice = parseFloat(
											addProductForm.desiredPrice.toFixed(2)
										);
									}
								}}
							>
								{#snippet left()}
									<DollarOutline class="h-5 w-5 text-gray-500 dark:text-gray-400" />
								{/snippet}
							</Input>
						</Label>
					</div>
					{#if addProductForm.productImage}
						<Img
							src={addProductForm.productImage}
							alt="Product ID Example"
							class="max-w-xs self-start rounded-lg md:max-w-2xl md:self-center"
						/>
					{/if}
				</section>
				<Button
					type="submit"
					class="my-4 w-full hover:cursor-pointer"
					pill
					disabled={shouldDisableStep2}>Confirm Details</Button
				>
			</div>
		</form>
	{:else if currentStep === 3}
		<form class="container mx-auto" onsubmit={handleStep3Submit}>
			<div class="mx-2 md:mx-8">
				<Heading tag="h3" class="mb-2"
					><Span highlight="orange">Product Scrape Schedule</Span></Heading
				>
				<section class="flex flex-col-reverse justify-between gap-4 md:flex-row md:items-center">
					<Heading tag="h4" class="max-w-2xl">
						Step 3: Setup the schedule for scraping this product
					</Heading>
				</section>
				<Button
					type="submit"
					class="my-4 w-full hover:cursor-pointer"
					pill
					disabled={shouldDisableStep3}>Submit Schedule</Button
				>
			</div>
		</form>
	{:else if currentStep === 4}
		<h1>Step 4</h1>
	{/if}
</section>

<script lang="ts">
	import { goto } from '$app/navigation';
	import { Button, Card, Heading, Helper, Input, Label, P, Span, Toast } from 'flowbite-svelte';
	import {
		ArrowLeftOutline,
		ArrowRightOutline,
		CheckCircleSolid,
		CloseOutline,
		EnvelopeSolid,
		ExclamationCircleSolid,
		LockSolid
	} from 'flowbite-svelte-icons';
	import { z } from 'zod';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let email = $state<string | undefined>(undefined);
	let emailError = $state<string | undefined>(undefined);

	// State for showing/hiding toast notifications
	let showToast = $state(false);
	// State for toast message and type
	let toastMessage = $state('Password Reset email sent!');
	let toastType = $state<'error' | 'success'>('success');

	const handleSubmit = async () => {
		const emailSchema = z
			.string()
			.min(1, { message: 'Email is required' })
			.email({ message: 'Invalid Email address' });
		const result = emailSchema.safeParse(email);
		if (!result.success) {
			emailError = result.error.errors.at(0)?.message;
			return;
		}
		try {
			const response = await fetch(`/api/password-reset`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Accept: 'application/json'
				},
				body: JSON.stringify({ email: email }),
				credentials: 'include'
			});
			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || 'Failed to send password reset email');
			}
			toastMessage = 'Password reset email sent successfully!';
			toastType = 'success';
		} catch (error) {
			toastType = 'error';
			if (error instanceof Error) {
				console.error('Error sending password reset email:', error.message);
				toastMessage = error.message;
			} else {
				console.error('Unexpected error:', error);
				toastMessage = 'An unexpected error occurred';
			}
		} finally {
			showToast = true;
			setTimeout(() => {
				showToast = false;
			}, 5000);
		}
	};
</script>

<svelte:head>
	<title>Password Reset - PriceTracker</title>
	<meta name="description" content="Reset your password for your PriceTracker account" />
</svelte:head>

<Toast
	dismissable={false}
	color={toastType === 'success' ? 'emerald' : 'rose'}
	position="top-right"
	toastStatus={showToast}
>
	{#snippet icon()}
		{#if toastType === 'success'}
			<CheckCircleSolid class=" h-6 w-6" />
		{:else}
			<ExclamationCircleSolid class=" h-6 w-6" />
		{/if}
	{/snippet}
	{toastMessage}
</Toast>

<main
	class="flex min-h-screen w-full items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8 dark:bg-gray-900"
>
	<Card class="p-4 sm:p-6" size="lg">
		<Span class="flex items-center text-gray-500 dark:text-gray-400 cursor-pointer max-w-fit">
			<ArrowLeftOutline
				class="size-8"
				onclick={() => {
					goto('/', { replaceState: true });
				}}
			/>
			Back
		</Span>
		<section id="card-header" class="py-4">
			<Heading tag="h2" class="text-primary-600 flex items-center justify-start gap-0.5"
				>Reset Password <LockSolid class="text-primary-800 size-10" /></Heading
			>
			<P class="mt-2 max-w-xl text-gray-600 dark:text-gray-400">
				<Span>
					Enter your email address below and an email will be sent for you to reset your password.
				</Span>
				<Span>
					Make sure to check your spam or junk folder if you don’t see it within a few minutes.
				</Span>
			</P>
		</section>
		<Label class="space-y-1" for="email">
			<Span class="ml-1">Email Address</Span>
			<Input
				type="email"
				placeholder="example@email.com"
				size="md"
				class="ps-9"
				id="email"
				bind:value={email}
			>
				{#snippet left()}
					<EnvelopeSolid class="h-5 w-5" />
				{/snippet}
			</Input>
			{#if emailError}
				<Helper class="mt-2 flex items-center" color="red">
					<CloseOutline class="mr-1 inline-block" />
					<Span class="text-base">
						{emailError}
					</Span>
				</Helper>
			{/if}
		</Label>
		<Button class="mt-4" type="button" color="secondary" size="xl" onclick={handleSubmit}>
			<Span>Send Reset Link</Span>
			<ArrowRightOutline class="ms-2 size-6" />
		</Button>
	</Card>
</main>

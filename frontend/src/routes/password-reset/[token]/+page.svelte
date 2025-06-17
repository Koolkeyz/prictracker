<script lang="ts">
	import { z } from 'zod';
	import type { PageData } from './$types';
	import { Card, Input, Label, Helper, Button, Heading, P, Span } from 'flowbite-svelte';
	import { goto } from '$app/navigation';
	import { CloseOutline } from 'flowbite-svelte-icons';
	let { data }: { data: PageData } = $props();

	const tokenData = $derived(data.resetTokenData);

	$inspect('Token Data', tokenData);

	const schema = z
		.object({
			id: z.string(),
			email: z.string().email({ message: 'Invalid email address' }),
			newPassword: z.string().min(6, { message: 'Password must be at least 6 characters' }),
			confirmPassword: z.string().min(6, { message: 'Password must be at least 6 characters' })
		})
		.refine((data) => data.newPassword === data.confirmPassword, {
			message: 'Passwords do not match',
			path: ['confirmPassword']
		});

	let formData = $state({
		id: data.resetTokenData.id,
		email: data.resetTokenData.email,
		newPassword: undefined as undefined | string,
		confirmPassword: undefined as undefined | string
	});

	let formErrors = $state({
		newPassword: undefined as undefined | string,
		confirmPassword: undefined as undefined | string
	});

	const handleSubmit = async () => {
		try {
			const parsedData = schema.parse(formData);

			const response = await fetch(`/api/password-reset-change`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Accept: 'application/json'
				},
				body: JSON.stringify({
					...parsedData
				}),
				credentials: 'include'
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || 'Unknown error');
			}

			const successData = await response.json();
			console.log('Password reset successful:', successData);


			// goto(`/`, { replaceState: true });
		} catch (err) {
			if (err instanceof z.ZodError) {
				// Handle validation errors
				console.error('Validation error:', err.errors);
				formErrors = {
					newPassword: err.errors.find((e) => e.path.includes('newPassword'))?.message,
					confirmPassword: err.errors.find((e) => e.path.includes('confirmPassword'))?.message
				};
			} else {
				// Handle other errors
				console.error('Error during password reset:', err);
			}
		}
	};
</script>

<svelte:head>
	<title>Password Reset - PriceTracker</title>
	<meta name="description" content="Reset your password for your PriceTracker account" />
</svelte:head>

<main
	class="flex min-h-screen w-full items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8 dark:bg-gray-900"
>
	<Card class="space-y-4 p-6 sm:p-8 md:space-y-6" size="lg">
		<form
			class="flex flex-col space-y-6"
			onsubmit={(e) => {
				e.preventDefault();
				handleSubmit();
			}}
		>
			<div>
				<Heading tag="h3" class="text-gray-900 dark:text-white">Change Password</Heading>
				<P class="mt-1.5 max-w-prose font-normal text-gray-600 dark:text-gray-400">
					<Span>Create a strong password to keep your account secure.</Span>
					<Span>Make sure it’s something you haven’t used before.</Span>
				</P>
			</div>
			<Label class="space-y-2">
				<span>New password</span>
				<Input
					type="password"
					name="password"
					placeholder="•••••"
					required
					bind:value={formData.newPassword}
				/>
				{#if formErrors.newPassword}
					<Helper color="red" class="mt-1">
						<CloseOutline class="mr-1 inline-block" />
						<Span class="inline-block">
							{formErrors.newPassword}
						</Span>
					</Helper>
				{/if}
			</Label>

			<Label class="space-y-2">
				<span>Confirm password</span>
				<Input
					type="password"
					name="confirm-password"
					placeholder="•••••"
					required
					bind:value={formData.confirmPassword}
				/>
				{#if formErrors.confirmPassword}
					<Helper color="red" class="mt-1">
						<CloseOutline class="mr-1 inline-block" />
						<Span class="inline-block">
							{formErrors.confirmPassword}
						</Span>
					</Helper>
				{/if}
			</Label>

			<Button type="submit" class="w-full">Reset passwod</Button>
		</form>
	</Card>
</main>

<script module lang="ts">
	import { z } from 'zod';

	const passwordResetFormSchema = z.object({
		email: z.string().email('Invalid email address')
	});
</script>

<script lang="ts">
	import type { PageData } from './$types';
	import { toast } from 'svelte-sonner';
	import FormMessage, { type FormMessageType } from '$components/ui/FormMessage.svelte';
	let { data }: { data: PageData } = $props();

	const passwordResetForm = $state({
		email: '',
		error: {
			email: null as FormMessageType | null
		}
	});

	const submitPasswordReset = async (e: MouseEvent) => {
		e.preventDefault();
		try {
			const parsedForm = passwordResetFormSchema.parse({
				email: passwordResetForm.email
			});

			const response = await fetch(`/api/password-reset`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Accept: 'application/json'
				},
				body: JSON.stringify(parsedForm),
				credentials: 'include'
			});
			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || 'Password reset failed');
			}

            toast.success('Password reset link sent to your email');

		} catch (error) {
			if (error instanceof z.ZodError) {
				error.errors.forEach((err) => {
					if (err.path.includes('email')) {
						passwordResetForm.error.email = {
							type: 'error',
							message: err.message
						};
					}
				});
			} else {
				if (error instanceof Error) toast.error(error.message);
				else toast.error('An unexpected error occurred');
			}
		} finally {
			// Reset the form after submission
			passwordResetForm.email = '';
			passwordResetForm.error.email = null;
		}
	};
</script>

<main class="max-w-screen min-h-screen place-content-center place-items-center">
	<!-- Login Form -->
	<form class={['w-sm lg:w-md', 'bg-base-300 rounded-4xl px-12 py-10 shadow-2xl']}>
		<fieldset class="fieldset px-4">
			<legend class="fieldset-legend pb-2.5 pt-4 text-xl">Password Reset</legend>
			<p class="text-accent text-nowrap pb-4 text-xs">
				Forgot your password? Reset it by entering your email below
			</p>
			<label class="label ml-1.5" for="email">Email</label>
			<input
				id="email"
				type="email"
				class="input w-full"
				placeholder="Enter email"
				bind:value={passwordResetForm.email}
			/>
			{#if passwordResetForm.error.email}
				<FormMessage
					type={passwordResetForm.error.email.type}
					message={passwordResetForm.error.email.message}
				/>
			{/if}
			<button class="btn btn-primary mt-4 text-base" onclick={submitPasswordReset}
				>Reset Password</button
			>
		</fieldset>
	</form>
</main>

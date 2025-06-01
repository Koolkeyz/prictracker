<script lang="ts" module>
	import { z } from 'zod';

	const loginFormSchema = z.object({
		email: z.string(),
		password: z.string().min(6, 'Password must be at least 6 characters long')
	});

	const signInRequest = async (data: {
		body: {
			username: string;
			password: string;
		};
	}): Promise<{ access_token: string; token_type: string }> => {
		const body = new URLSearchParams({
			grant_type: 'password',
			username: data.body.username,
			password: data.body.password,
			scope: '',
			client_id: '',
			client_secret: ''
		});

		const response = await fetch(`/api/token`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				Accept: 'application/json'
			},
			body: body,
			credentials: 'include'
		});

		if (!response.ok) {
			const errorData = await response.json();
			throw new Error(`${errorData.detail || 'Unknown error'}`);
		}

		const tokenData = await response.json();
		return {
			access_token: tokenData.access_token,
			token_type: tokenData.token_type
		};
	};
</script>

<script lang="ts">
	import { toast } from 'svelte-sonner';
	import FormMessage, { type FormMessageType } from '$components/ui/FormMessage.svelte';
	import Icon from '$components/ui/Icon.svelte';
	import { goto } from '$app/navigation';
	const loginForm = $state({
		email: '',
		password: '',
		error: {
			email: null as FormMessageType | null,
			password: null as FormMessageType | null
		}
	});

	let isSigningIn = $state(false);

	async function signInUser(e: MouseEvent) {
		e.preventDefault();
		isSigningIn = true; // Set the signing in state to true
		try {
			const parsedForm = loginFormSchema.parse(loginForm);

			await signInRequest({
				body: {
					username: parsedForm.email,
					password: parsedForm.password
				}
			});

			// Proceed with login logic, e.g., API call
			setTimeout(() => {
				toast.success('Login successful!', {
					description: 'You have successfully logged in.',
					dismissable: true,
					duration: 2000
				});
				loginForm.error.email = null; // Clear email error
				loginForm.error.password = null; // Clear password error
			}, 3000);

			setTimeout(() => {
				isSigningIn = false; // Reset the signing in state
				goto('/dashboard'); // Redirect to dashboard or another page after successful login
			}, 4000);
		} catch (error) {
			if (error instanceof z.ZodError) {
				error.errors.forEach((err) => {
					if (err.path.includes('email')) {
						loginForm.error.email = {
							type: 'error',
							message: err.message
						};
					} else if (err.path.includes('password')) {
						if (err.code === 'too_small') {
							loginForm.error.password = {
								type: 'error',
								message: 'Password must be at least 6 characters long'
							};
						} else {
							loginForm.error.password = {
								type: 'error',
								message: err.message
							};
						}
					}
				});
			} else if (error instanceof Error) {
				// Handle other errors, such as network issues or server errors
				toast.error(error.message, {
					description: 'Please check your credentials and try again.'
				});
			} else {
				toast.error('An unexpected error occurred. Please try again later.');
			}
		} finally {
			// Reset the form if needed
			// loginForm.email = '';
			// loginForm.password = '';

		}
	}
</script>

<main class="max-w-screen min-h-screen place-content-center place-items-center">
	{#if isSigningIn}
		<section>
			<Icon name="svg-spinners--blocks-shuffle-3" class="text-primary size-80 place-self-center" />
		</section>
	{:else}
		<!-- Login Form -->
		<form class={['w-sm lg:w-md', 'bg-base-300 rounded-4xl px-12 py-10 shadow-2xl']}>
			<fieldset class="fieldset px-4">
				<legend class="fieldset-legend py-4 text-xl">Login</legend>
				<label class="label" for="email">Email</label>
				<input
					id="email"
					type="email"
					class="input w-full"
					placeholder="Email"
					bind:value={loginForm.email}
				/>
				{#if loginForm.error.email}
					<!-- <p class="mt-1 text-sm text-red-500">{loginForm.error.email}</p> -->
					<FormMessage type={loginForm.error.email.type} message={loginForm.error.email.message} />
				{/if}
				<label class="label" for="password">Password</label>
				<input
					id="password"
					type="password"
					class="input w-full"
					placeholder="Password"
					bind:value={loginForm.password}
				/>
				{#if loginForm.error.password}
					<FormMessage
						type={loginForm.error.password.type}
						message={loginForm.error.password.message}
					/>
				{/if}

				<a class="link link-hover" href="/password-reset">Forgot password?</a>
				<button class="btn btn-primary mt-4 text-base" onclick={signInUser}>Login</button>
			</fieldset>
		</form>
	{/if}
</main>

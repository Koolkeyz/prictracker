import { error, redirect } from '@sveltejs/kit';
import type { LayoutLoad } from './$types';
import { UserSchema } from '$schemas/user.schema';

export const load = (async ({ fetch }) => {
	// Fetch the authenticated user data
	const response = await fetch('/api/auth-user', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		credentials: 'include'
	});

	if (!response.ok) redirect(303, '/');

	const userData = await response.json();

	const authUser = UserSchema.safeParse(userData);
	if (!authUser.success) error(500, 'Invalid user data format');
	
	return {
		authUser: authUser.data
	};
}) satisfies LayoutLoad;

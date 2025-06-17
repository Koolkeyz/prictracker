import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { UserSchema } from '$schemas/user.schema';
import { z } from 'zod';

const validationResponseSchema = UserSchema.pick({
	email: true,
	username: true
}).extend({
	token: z.string(),
	id: z.string()
});

export const load = (async ({ params, fetch }) => {
	const { token } = params;

	const response = await fetch(`/api/validate-reset-token`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		},
		body: JSON.stringify({ token }),
		credentials: 'include'
	});

	if (!response.ok) error(400, 'Invalid or expired token');

	const data = await response.json();

    const parsedData = validationResponseSchema.safeParse(data);

    if (!parsedData.success) error(400, 'Invalid response from server');

	return {
        resetTokenData: parsedData.data
    };
}) satisfies PageLoad;

import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load = (async ({ parent }) => {
    const { authenticatedUser } = await parent();

    if (!authenticatedUser) {
        error(401, 'Unauthorized access to dashboard');
    }

    return { authenticatedUser };
}) satisfies PageLoad;



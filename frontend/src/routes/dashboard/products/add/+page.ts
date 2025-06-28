import type { PageLoad } from './$types';

export const load = (async ({ parent }) => {
	const { authUser } = await parent();
	return { authUser };
}) satisfies PageLoad;

import type { LayoutLoad } from './$types';
import { UserModel } from '$lib/models';
import { redirect } from '@sveltejs/kit';

export const load = (async ({ fetch }) => {
    const getUser = async () => {
        try {
            const response = await fetch('/api/auth-user',
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                    credentials: 'include'
                }
            )

            if (!response.ok) {
                redirect(302, '/')
            }

            const userData = await response.json();
            const user = UserModel.parse(userData);

            return user;

        } catch (error) {
            if (error instanceof Error) {
                console.error('Error fetching user:', error.message);
                throw error;
            } else {
                console.error('An unexpected error occurred while fetching user data');
                throw new Error('An unexpected error occurred');
            }
        }
    }

    const authenticatedUser = await getUser();



    return { authenticatedUser };
}) satisfies LayoutLoad;
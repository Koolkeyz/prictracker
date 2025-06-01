import { ConfigModel } from '$lib/models';
import type { PageLoad } from './$types';

export const load = (async ({ fetch }) => {
    const getUserAgents = async () => {
        try {
            const response = await fetch('/api/config/user-agents',
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                    credentials: 'include'
                }
            );
            if (!response.ok) {
                throw new Error('Failed to fetch user agents');
            }
            const config = ConfigModel.parse(await response.json());
            return config.userAgents || [];
        } catch (error) {
            if (error instanceof Error) {
                console.error('Error fetching user agents:', error.message);
            }
            return [];
        }
    };

    const getProxyServers = async () => {
        try {
            const response = await fetch('/api/config/proxy-servers', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                credentials: 'include'
            });
            if (!response.ok) {
                throw new Error('Failed to fetch proxy servers');
            }
            const data = ConfigModel.parse(await response.json());

            return data.proxyServers || [];
        } catch (error) {
            if (error instanceof Error) {
                console.error('Error fetching proxy servers:', error.message);
            }
            return [];
        }
    };

    const userAgents = await getUserAgents();
    const proxyServers = await getProxyServers();


    return { userAgents, proxyServers };
}) satisfies PageLoad;
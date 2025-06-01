import { z } from 'zod';

export const UserModel = z.object({
    _id: z.string().transform((val) => val.toString()),
    role: z.enum(['admin', 'user']),
    email: z.string().email(),
    username: z.string(),
    password: z.string().nullable().transform((val) => val != '' ? val : null),
    firstName: z.string().optional(),
    lastName: z.string().optional(),
    avatar: z.string().optional().nullable(),
    createdAt: z.string().transform((val) => new Date(val)),
})

export const ConfigModel = z.object({
    _id: z.string().transform((val) => val.toString()),
    userAgents: z.array(z.string()).optional(),
    proxyServers: z.array(z.string()).optional(),
})
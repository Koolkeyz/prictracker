import { z } from 'zod';

export const UserSchema = z.object({
	avatar: z.string().nullable().default(null),
	email: z.string().email(),
	createdAt: z.union([
		z.string().refine((val) => !isNaN(Date.parse(val)), { message: 'Invalid datetime format' }),
		z.date()
	]),
	forcePasswordChange: z.boolean(),
	firstName: z.string().min(1),
	lastName: z.string().min(1),
	password: z.string().optional(),
	role: z.enum(['admin', 'user']),
	username: z.string().min(1),
	_id: z.string()
});

export type UserSchemaType = z.infer<typeof UserSchema>;

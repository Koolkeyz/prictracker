import { z } from 'zod';

export const ProductSchema = z.object({
	id: z.string().uuid(),
	user_id: z.string().uuid(),
	platform: z.enum(['amazon', 'ebay', 'newegg']),
	product_link: z.string().url(),
	product_name: z.string(),
	product_image: z.string().url(),
	created_at: z.string().datetime(),
	updated_at: z.string().datetime(),
	product_tracking: z.array(
		z.object({
			price: z.number(),
			timestamp: z.string().datetime(),
			seller: z
				.object({
					ships_from: z.string().optional(),
					sold_by: z.string().optional()
				})
				.optional(),
			coupon: z
				.object({
					value: z.number(),
					discount_type: z.enum(['percentage', 'fixed'])
				})
				.optional()
		})
	)
});

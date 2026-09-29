import { z } from "zod";
const schema=z.object({NEXT_PUBLIC_SUPABASE_URL:z.string().url(),NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY:z.string().min(1),ASTROLOGY_API_URL:z.string().url().default("http://localhost:8000")});
export function getEnv(){return schema.parse({NEXT_PUBLIC_SUPABASE_URL:process.env.NEXT_PUBLIC_SUPABASE_URL,NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY:process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY,ASTROLOGY_API_URL:process.env.ASTROLOGY_API_URL})}

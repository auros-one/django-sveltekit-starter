import { createClient } from '@supabase/supabase-js';
// Using Environment Variables in SvelteKit: https://joyofcode.xyz/sveltekit-environment-variables
// We're using public env vars so the client can be used client-side
import { PUBLIC_SUPABASE_PROJECT_URL, PUBLIC_SUPABASE_PUBLIC_API_KEY } from '$env/static/public';

export const supabase = createClient(PUBLIC_SUPABASE_PROJECT_URL, PUBLIC_SUPABASE_PUBLIC_API_KEY);

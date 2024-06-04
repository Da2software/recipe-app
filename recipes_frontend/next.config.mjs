/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        RECIPES_API: process.env.RECIPES_API,
        USERS_API: process.env.USERS_API
    }
};

export default nextConfig;

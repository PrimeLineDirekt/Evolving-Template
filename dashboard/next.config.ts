import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Disable React Strict Mode to prevent double renders
  reactStrictMode: false,
  // Fix Turbopack workspace root detection (multiple lockfiles issue)
  turbopack: {
    root: '.',
  },
  // Webpack config to exclude certain paths from watching
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        ...config.watchOptions,
        poll: 1000, // Check for changes every second instead of using native watchers
        aggregateTimeout: 500, // Delay rebuild after first change
        ignored: [
          '**/node_modules/**',
          '**/.git/**',
          '**/logs/**',
          '**/knowledge/**',
          '**/.next/**',
          '**/workflows/**',
          '**/_inbox/**',
          '**/_handoffs/**',
        ],
      };
    }
    return config;
  },
};

export default nextConfig;

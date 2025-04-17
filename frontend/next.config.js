// next.config.js

/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",              // intercept frontend calls to /api/*
        destination: "http://localhost:8000/api/:path*", // redirect to FastAPI
      },
    ]
  },
}

module.exports = nextConfig

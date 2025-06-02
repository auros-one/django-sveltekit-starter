# Frontend Dockerfile for SvelteKit application
FROM node:20-alpine AS base

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Development stage
FROM base AS development
# Install all dependencies including dev
RUN npm ci

# Expose Vite dev server port
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Build stage
FROM base AS build
# Install all dependencies for build
RUN npm ci

# Build the application
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Copy built application
COPY --from=build /app/build ./build
COPY --from=build /app/package*.json ./

# Install only production dependencies
RUN npm ci --only=production && npm cache clean --force

# Expose port
EXPOSE 3000

# Start production server
CMD ["node", "build"]
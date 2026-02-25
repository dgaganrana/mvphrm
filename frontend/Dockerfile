# Stage 1: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Install build tools for native dependencies
# RUN apk add --no-cache python3 make g++ libc6-compat

# Copy only dependency manifests first (better caching)
COPY package.json package-lock.json ./
RUN npm ci

# Copy only required source files
COPY next.config.ts ./
COPY tsconfig.json ./
COPY public ./public
COPY src ./src

# Build Next.js app
ARG NEXT_PUBLIC_BACKEND_URL
ENV NEXT_PUBLIC_BACKEND_URL=$NEXT_PUBLIC_BACKEND_URL
RUN npm run build

# Stage 2: Runner
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Copy build artifacts and production dependencies
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/next.config.ts ./next.config.ts

EXPOSE 3000
CMD ["npm", "run", "start"]

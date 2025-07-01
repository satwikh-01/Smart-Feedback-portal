# Builder stage
FROM node:20-slim AS builder
WORKDIR /app

# Install dependencies
COPY client/package.json client/yarn.lock* client/package-lock.json* client/pnpm-lock.yaml* ./
RUN \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i --frozen-lockfile; \
    else echo "Lockfile not found." && exit 1; \
    fi

# Copy source code
COPY client/ .

# Build the Next.js app
RUN npm run build

# Final stage
FROM node:20-slim AS final
WORKDIR /app

# Copy built assets from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

# Expose the port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]

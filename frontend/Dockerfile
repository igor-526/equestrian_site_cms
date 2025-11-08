ARG NEXT_PUBLIC_BACKEND_URL

FROM node:20-alpine AS deps

WORKDIR /app

COPY package.json package-lock.json* ./

RUN apk add --no-cache libc6-compat \
    && npm ci

FROM node:20-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ARG NEXT_PUBLIC_BACKEND_URL
ENV NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL}
ENV NODE_ENV=production

RUN npm run build
RUN npx next export

FROM nginx:1.27-alpine AS runner

ARG NEXT_PUBLIC_BACKEND_URL
ENV NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL}

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/out /usr/share/nginx/html

EXPOSE 80
ENV NODE_ENV=production

CMD ["nginx", "-g", "daemon off;"]



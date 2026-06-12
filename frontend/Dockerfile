FROM node:24-slim

ENV PNPM_HOME=/pnpm \
    PATH="/pnpm:$PATH"

WORKDIR /app

RUN corepack enable

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

EXPOSE 3002

CMD ["pnpm", "dev", "--host", "0.0.0.0"]

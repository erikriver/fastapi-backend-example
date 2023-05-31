FROM node:16 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

# Build and serve the Next.js project
RUN npm run build

CMD npm run start

EXPOSE 3000
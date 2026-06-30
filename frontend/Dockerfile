FROM node:22-alpine AS build

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ .

ENV PUBLIC_API_URL=
ENV PUBLIC_SITE_URL=https://reporili.tech

RUN npm run build

FROM nginx:alpine

RUN apk add --no-cache gettext

COPY deploy/nginx.conf.template /etc/nginx/nginx.conf.template
COPY deploy/nginx-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

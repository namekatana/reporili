FROM node:22-alpine AS build

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ .

ARG PUBLIC_API_URL=
ARG PUBLIC_SITE_URL=https://reporili.tech
ARG PUBLIC_GITHUB_URL=https://github.com/namekatana/reporili
ARG PUBLIC_GOOGLE_SITE_VERIFICATION=

ENV PUBLIC_API_URL=$PUBLIC_API_URL
ENV PUBLIC_SITE_URL=$PUBLIC_SITE_URL
ENV PUBLIC_GITHUB_URL=$PUBLIC_GITHUB_URL
ENV PUBLIC_GOOGLE_SITE_VERIFICATION=$PUBLIC_GOOGLE_SITE_VERIFICATION

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

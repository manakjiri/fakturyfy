FROM python:3.11-alpine AS base
FROM node:lts-alpine AS vue-build
WORKDIR /vue-app

COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm run build-only -- --outDir dist


FROM base AS backend-build
WORKDIR /app

COPY backend/requirements.txt requirements.txt
COPY backend/external external
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .
RUN rm -rf external


FROM base AS final
WORKDIR /app

COPY --from=backend-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-build /app .
COPY --from=vue-build /vue-app/dist fakturyfy/app/templates

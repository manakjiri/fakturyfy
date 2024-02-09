FROM node:lts-alpine AS vue-build
WORKDIR /vue-app

COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm run build-only -- --outDir dist


FROM python:3.11-alpine AS final
WORKDIR /app

COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .
COPY --from=vue-build /vue-app/dist fakturyfy/app/templates

FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN ls -l /app    # <-- Aquí verificas que los archivos se copiaron bien
RUN npm install
COPY . .
EXPOSE 3001
CMD ["node", "index.js"]

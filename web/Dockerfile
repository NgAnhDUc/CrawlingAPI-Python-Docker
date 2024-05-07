FROM node:latest

EXPOSE 3000

WORKDIR /app

RUN npm i npm@latest

COPY package*.json package-lock.json ./

RUN npm install 

COPY . .

CMD [ "node", "index.js" ]
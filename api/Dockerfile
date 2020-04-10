FROM node:12

RUN mkdir -p /usr/safetrace/api
WORKDIR /usr/safetrace/api

COPY . .

RUN npm install

EXPOSE ${PORT}
CMD [ "npm", "run", "start" ]
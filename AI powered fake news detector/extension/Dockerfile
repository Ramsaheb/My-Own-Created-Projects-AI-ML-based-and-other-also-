FROM node:16-alpine

WORKDIR /app

# Copy extension files
COPY . .

# Install http-server for serving the extension files
RUN npm install -g http-server

# Expose port for http-server
EXPOSE 8080

# Start http-server
CMD ["http-server", "-p", "8080"]
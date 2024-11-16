# Use an official Node.js image to build the React app
FROM node:18 AS build

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Expose (Vite) React development server port
EXPOSE 5173

# Start React development server (with hot reloading)
CMD ["npm", "run", "dev"]

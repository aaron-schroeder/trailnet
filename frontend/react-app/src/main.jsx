import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'
import CustomApolloProvider from './ApolloProvider'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <CustomApolloProvider>
      <App />
    </CustomApolloProvider>
  </StrictMode>
);

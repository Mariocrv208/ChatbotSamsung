import React from 'react';
import Chatbot from './components/Chatbot';

export default function App() {
  return (
    <div className="app-root">
      <header className="app-header">
        <h1>Chatbot Samsung Demo</h1>
      </header>

      <main className="app-main">
        <Chatbot />
      </main>

      <footer className="app-footer">
        <small>Hecho por Loopers</small>
      </footer>
    </div>
  );
}
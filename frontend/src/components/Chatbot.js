import React, { useEffect, useRef, useState } from 'react';
import Message from './Message';

// Helper to generate ids
const uid = () => Math.random().toString(36).slice(2, 9);

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { id: uid(), role: 'bot', text: '¡Hola! Soy tu chatbot. ¿En qué puedo ayudarte?', timestamp: Date.now() }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef();

  // Auto-scroll when messages change
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  // Simulated backend response (mock). Replace this with fetch() to your API.
  const fetchBotReplyMock = async (userText) => {
    // Simula latencia y produce una respuesta simple
    await new Promise(res => setTimeout(res, 700 + Math.random() * 700));
    // Respuesta simple: espejo + frase
    return `Has dicho: "${userText}". Esta es una respuesta de ejemplo.`;
  };

  // Enviar mensaje
  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg = { id: uid(), role: 'user', text, timestamp: Date.now() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // --- ejemplo mock (ya incluido) ---
      const botText = await fetchBotReplyMock(text);


      const botMsg = { id: uid(), role: 'bot', text: botText, timestamp: Date.now() };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      const errMsg = { id: uid(), role: 'bot', text: 'Error: no se pudo obtener respuesta. Intenta otra vez.', timestamp: Date.now() };
      setMessages(prev => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  // Enviar con Enter (Shift+Enter para nueva línea)
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Limpiar chat
  const clearChat = () => {
    setMessages([{ id: uid(), role: 'bot', text: 'Chat reiniciado. ¿En qué puedo ayudarte?', timestamp: Date.now() }]);
  };

  return (
    <div className="chat-fixed-container">
        <div className="chat-wrapper" role="application" aria-label="Chatbot">
        <div className="chat-window" ref={scrollRef}>
            {messages.map(m => <Message key={m.id} message={m} />)}
            {loading && (
            <div className="message-row bot">
                <div className="avatar">B</div>
                <div className="bubble">
                <div className="bubble-text typing">
                    <span className="dot" /> <span className="dot" /> <span className="dot" />
                </div>
                </div>
            </div>
            )}
        </div>
      </div>

      <div className="chat-controls">
        <textarea
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Escribe un mensaje... (Enter para enviar, Shift+Enter nueva línea)"
          rows={1}
          aria-label="Mensaje"
        />
        <div className="controls-right">
          <button onClick={clearChat} className="btn secondary" aria-label="Limpiar chat">Limpiar</button>
          <button onClick={handleSend} className="btn primary" aria-label="Enviar mensaje" disabled={loading || input.trim() === ''}>
            {loading ? 'Enviando…' : 'Enviar'}
          </button>
        </div>
      </div>
    </div>
  );
}

import React from 'react';

export default function Message({ message }) {
  // message: { id, text, role: 'user'|'bot', timestamp }
  const isUser = message.role === 'user';
  return (
    <div className={`message-row ${isUser ? 'user' : 'bot'}`}>
      <div className="avatar" aria-hidden>
        {isUser ? 'U' : 'B'}
      </div>
      <div className="bubble">
        <div className="bubble-text">{message.text}</div>
        <div className="bubble-meta">
          <span className="time">
            {new Date(message.timestamp).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}
          </span>
        </div>
      </div>
    </div>
  );
}

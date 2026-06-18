import { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import ChatBubble from './components/ChatBubble';
import TypingIndicator from './components/TypingIndicator';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const initialMessages = [
  {
    id: 'welcome',
    role: 'ai',
    text: 'Hello! Ask me anything about your PDF content and I will find the answer for you.',
  },
];

export default function App() {
  const [messages, setMessages] = useState(initialMessages);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const question = inputValue.trim();
    if (!question || loading) return;

    setErrorMessage(null);
    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        question,
      });

      const aiMessage = {
        id: `ai-${Date.now()}`,
        role: 'ai',
        text: response.data.answer,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      setErrorMessage(
        error?.response?.data?.detail || 'Unable to contact the chatbot API.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      handleSubmit(event);
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-icon">
            <div className="brand-icon-file">
              <span>PDF</span>
            </div>
          </div>
          <div>
            <h1>PDF RAG Chatbot</h1>
            <p>Ask questions about your uploaded PDFs.</p>
          </div>
        </div>

        <div className="sidebar-card">
          <p>Upload your documents and get instant, accurate answers backed by retrieved content.</p>
        </div>
      </aside>

      <main className="chat-panel">
        <div className="chat-header">
          <div>
            <p className="chat-label">AI Assistant</p>
            <h2>Ask anything from PDFs</h2>
          </div>
        </div>

        <div className="chat-window">
          {messages.map((message) => (
            <ChatBubble key={message.id} role={message.role} text={message.text} />
          ))}
          {loading && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        {errorMessage && <div className="error-banner">{errorMessage}</div>}

        <form className="chat-form" onSubmit={handleSubmit}>
          <textarea
            className="chat-input"
            placeholder="Type your question here..."
            value={inputValue}
            onChange={(event) => setInputValue(event.target.value)}
            onKeyDown={handleKeyDown}
            rows={2}
            disabled={loading}
          />
          <button className="send-button" type="submit" disabled={loading || !inputValue.trim()}>
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </main>
    </div>
  );
}

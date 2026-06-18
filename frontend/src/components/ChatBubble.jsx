export default function ChatBubble({ role, text }) {
  const isUser = role === 'user';

  return (
    <div className={`message-row ${isUser ? 'message-row-user' : 'message-row-ai'}`}>
      <div className={`message-bubble ${isUser ? 'user-bubble' : 'ai-bubble'}`}>
        {text}
      </div>
    </div>
  );
}

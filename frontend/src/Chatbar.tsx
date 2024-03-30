import React, { useState } from 'react';
import axios from 'axios';

const ChatBar: React.FC = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleMessageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };

  const handleSendMessage = async () => {
    try {
      console.log(message)
      const { data } = await axios.post('http://localhost:8000/chat', { message });
      setResponse(data.response);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={message}
        onChange={handleMessageChange}
        placeholder="Type your message..."
      />
      <button onClick={handleSendMessage}>Send</button>
      <p>Response: {response}</p>
    </div>
  );
};

export default ChatBar;

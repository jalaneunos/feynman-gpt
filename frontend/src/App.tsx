import React from 'react';
import UploadButton from './UploadButton';
import ChatBar from './Chatbar';

const App: React.FC = () => {
  return (
    <div>
      <h1>My App</h1>
      <UploadButton />
      <ChatBar />
    </div>
  );
};

export default App;

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UploadButton from './UploadButton';
import LearningPage from './LearningPage';

const App: React.FC = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<UploadButton />} />
          <Route path="/learning" element={<LearningPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

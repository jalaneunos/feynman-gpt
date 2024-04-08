import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LearningPage from "./LearningPage";
import LandingPage from "./LandingPage";
import Header from "./Header";

const App: React.FC = () => {
    return (
        <Router>
            <div className="flex flex-col min-h-screen">
                <Header />
                <main className="flex-grow">
                    <Routes>
                        <Route path="/" element={<LandingPage />} />
                        <Route path="/learning" element={<LearningPage />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
};
export default App;

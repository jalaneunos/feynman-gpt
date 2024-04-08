// Header.tsx

import React from "react";
import { Link } from "react-router-dom";

const Header: React.FC = () => {
    return (
        <header>
            <div className="max-w-7xl py-4 px-4 sm:px-6 lg:px-8 flex items-center">
                <Link to="/" className="flex items-center">
                    <img src="/logo.png" alt="FeynmanGPT Logo" className="h-8 w-auto" />
                    <span className="text-xl font-bold text-gray-900">eynmanGPT</span>
                </Link>
            </div>
        </header>
    );
};

export default Header;

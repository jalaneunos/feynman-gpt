import React from "react";

const Loading: React.FC = () => {
    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <div className="animate-spin rounded-full h-24 w-24 border-t-2 border-b-2 border-red-500"></div>
            <p className="mt-4 text-xl">Loading...this may take a minute</p>
        </div>
    );
};

export default Loading;

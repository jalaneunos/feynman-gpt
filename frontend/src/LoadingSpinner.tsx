import React from "react";

const LoadingSpinner: React.FC = () => {
    return (
        <div className="flex justify-center mt-2">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-red-500 p-2"></div>
        </div>
    );
};

export default LoadingSpinner;

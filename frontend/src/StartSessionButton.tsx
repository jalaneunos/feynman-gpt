import React from "react";

interface StartSessionButtonProps {
    onClick: () => void;
}

const StartSessionButton: React.FC<StartSessionButtonProps> = ({ onClick }) => {
    return (
        <button onClick={onClick} className="btn">
            Start
        </button>
    );
};

export default StartSessionButton;

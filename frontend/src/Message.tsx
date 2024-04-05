import React, { useEffect, useRef } from "react";

interface MessageProps {
    text: string;
    sender: "You" | "Richie" | "Timmy";
}

const Message: React.FC<MessageProps> = ({ text, sender }) => {
    const messageClass = sender === "You" ? "bg-[#f4f3ee] self-end" : "bg-gray-100 self-start";
    const senderColor = sender === "You" ? "text-black" : sender === "Richie" ? "text-warning" : "text-primary";
    const fontWeight = sender === "You" ? "" : "font-semibold";
    const messageRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (messageRef.current) {
            messageRef.current.classList.add("opacity-0", "transform", "scale-50");
            setTimeout(() => {
                messageRef.current?.classList.remove("opacity-0", "transform", "scale-50");
                messageRef.current?.classList.add("opacity-100", "scale-100");
            }, 100);
        }
    }, []);

    return (
        <div
            ref={messageRef}
            className={`mb-2 px-3 py-2 rounded-lg transition-all duration-500 ease-in-out ${messageClass}`}
        >
            <div className={`font-bold ${senderColor}`}>{sender}</div>
            <div className={fontWeight}>{text}</div>
        </div>
    );
};

export default Message;

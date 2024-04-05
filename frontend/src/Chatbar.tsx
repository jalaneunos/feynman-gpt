import React, { useState, useRef, useEffect } from "react";
import { FiSend } from "react-icons/fi";

interface Message {
    text: string;
    sender: "You" | "Richie" | "Timmy";
}

interface ChatBarProps {
    onSendMessage: (message: string) => void;
    messages: Message[];
}

const ChatBar: React.FC<ChatBarProps> = ({ onSendMessage }) => {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState<Message[]>([]);
    const chatContainerRef = useRef<HTMLDivElement>(null);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleMessageChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setMessage(event.target.value);
    };

    const handleSendMessage = () => {
        if (message.trim() !== "") {
            onSendMessage(message);
            setMessage("");
        }
    };

    const handleKeyPress = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleSendMessage();
        }
    };

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [message]);

    return (
        <>
            <textarea
                ref={textareaRef}
                value={message}
                onChange={handleMessageChange}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 p-2 border-none rounded-md mr-2 resize-none"
                rows={1}
            />
            <button onClick={handleSendMessage} className="btn cursor-pointer">
                <FiSend size={20} />
            </button>
        </>
    );
};

export default ChatBar;

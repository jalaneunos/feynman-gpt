import React, { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import ChatBar from "./Chatbar";
import Message from "./Message";
import StartSessionButton from "./StartSessionButton";
import Loading from "./Loading";
import LoadingSpinner from "./LoadingSpinner";
import { useLocation } from "react-router-dom";

interface Message {
    text: string;
    sender: "You" | "Timmy" | "Richie";
}

const LearningPage: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLearningStarted, setIsLearningStarted] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [questionIndex, setQuestionIndex] = useState(-1);
    const [title, setTitle] = useState(null);
    const chatContainerRef = useRef<HTMLDivElement>(null);
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const sessionId = searchParams.get("sessionId");

    const startLearningSession = useCallback(async () => {
        if (sessionId) {
            try {
                const response = await axios.get(
                    `${process.env.REACT_APP_BACKEND_URL}/start_learning?session_id=${encodeURIComponent(sessionId)}`
                );
                setTitle(response.data.data.title);
                const richieIntroduction = response.data.data.introductory_messages[0];
                const timmyIntroduction = response.data.data.introductory_messages[1];
                setQuestionIndex(0);
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: richieIntroduction, sender: "Richie" },
                    { text: timmyIntroduction, sender: "Timmy" },
                ]);
            } catch (error) {
                console.error("Error starting learning session:", error);
            }
        }
    }, [sessionId]);

    useEffect(() => {
        startLearningSession();
    }, [startLearningSession]);

    const handleStartLearning = async () => {
        try {
            const questionResponse = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/question`, {
                session_id: sessionId,
                question_index: 0,
            });
            const message = questionResponse.data.data.question;
            setMessages((prevMessages) => [...prevMessages, { text: message, sender: "Timmy" }]);
            setIsLearningStarted(true);
        } catch (error) {
            console.error("Error fetching first question:", error);
        }
    };

    const handleSendMessage = async (message: string) => {
        setMessages((prevMessages) => [...prevMessages, { text: message, sender: "You" }]);
        setIsLoading(true);
        try {
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/answer`, {
                session_id: sessionId,
                user_answer: message,
                question_index: questionIndex,
            });

            if (response.data.status === "success") {
                if (response.data.data.next_question_index !== undefined) {
                    const nextQuestionIndex = response.data.data.next_question_index;
                    setQuestionIndex(nextQuestionIndex);
                    const questionResponse = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/question`, {
                        session_id: sessionId,
                        question_index: nextQuestionIndex,
                    });
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { text: response.data.message, sender: "Timmy" },
                        { text: questionResponse.data.data.question, sender: "Timmy" },
                    ]);
                } else {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { text: "Congratulations! You have completed the learning session.", sender: "Richie" },
                    ]);
                }
            } else {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: response.data.message, sender: "Richie" },
                    { text: response.data.data.guidance, sender: "Richie" },
                ]);
            }
            setIsLoading(false);
        } catch (error) {
            setIsLoading(false);
            console.error("Error submitting answer:", error);
        }
    };

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    if (questionIndex === -1) {
        return <Loading />;
    }

    return (
        <div className="flex flex-col h-screen">
            <div className="flex-1 overflow-y-auto">
                <div className="max-w-2xl mx-auto w-full px-4">
                    <div className="flex justify-center pt-3">
                        <h2 className="text-xl mb-4">{title}</h2>
                    </div>
                    <div ref={chatContainerRef} className="mb-20">
                        {messages.map((msg, index) => (
                            <Message key={index} text={msg.text} sender={msg.sender} />
                        ))}
                        {isLoading && <LoadingSpinner />}
                    </div>
                </div>
            </div>
            <div className="fixed bottom-0 left-0 right-0 p-4">
                <div className="max-w-2xl mx-auto flex justify-center">
                    {!isLearningStarted ? (
                        <StartSessionButton onClick={handleStartLearning} />
                    ) : (
                        <ChatBar onSendMessage={handleSendMessage} messages={messages} />
                    )}
                </div>
            </div>
        </div>
    );
};

export default LearningPage;

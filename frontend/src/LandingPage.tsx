import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Portrait from "./Portrait";
import Loading from "./Loading";

const LandingPage: React.FC = () => {
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setIsLoading(true);
            const formData = new FormData();
            formData.append("file", event.target.files[0]);

            try {
                const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/index_document`, formData);
                const sessionId = response.data.data.session_id;
                navigate(`/learning?sessionId=${encodeURIComponent(sessionId)}`);
            } catch (error) {
                console.error("Error uploading file:", error);
                setIsLoading(false);
            }
        }
    };

    if (isLoading) {
        return <Loading />;
    }
    return (
        <div className="flex flex-col items-center justify-center h-screen p-8">
            <h1 className="text-6xl font-semibold mb-24">
                Learn via the{" "}
                <a
                    href="https://fs.blog/feynman-technique/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="feynman-link"
                >
                    Feynman Technique
                    <span className="black-underline" />
                </a>
                , now enhanced with LLMs.
            </h1>
            <div className="flex items-center justify-evenly w-full">
                <div className="text-5xl" style={{ lineHeight: 1.4 }}>
                    <p>
                        We learn the most by teaching others.
                        <br />
                        Can you teach Timmy?
                    </p>
                    <p>
                        <label
                            htmlFor="file-upload"
                            style={{
                                color: "green",
                                position: "relative",
                                cursor: "pointer",
                                display: "inline-block",
                            }}
                            className="upload-label"
                        >
                            Upload
                            <span className="underline"></span>
                        </label>{" "}
                        your study materials to get started.
                    </p>
                    <input id="file-upload" type="file" onChange={handleFileChange} style={{ display: "none" }} />
                </div>
                <div className="flex space-x-8">
                    <Portrait imageSrc="/timmy_dp.webp" name="Timmy" />
                    <Portrait imageSrc="/richie_dp.webp" name="Richie" />
                </div>
            </div>
            <style>
                {`
                    .upload-label:hover .underline,
                    .feynman-link:hover .black-underline {
                        width: 100%;
                    }

                    .underline {
                        position: absolute;
                        bottom: 0;
                        left: 0;
                        width: 0;
                        height: 2px;
                        background-color: green;
                        transition: width 0.3s ease-in-out;
                    }

                    .black-underline {
                        position: absolute;
                        bottom: 0;
                        left: 0;
                        width: 0;
                        height: 2px;
                        background-color: black;
                        transition: width 0.3s ease-in-out;
                    }

                    .feynman-link {
                        color: black;
                        position: relative;
                        text-decoration: none;
                    }
                `}
            </style>
        </div>
    );
};

export default LandingPage;

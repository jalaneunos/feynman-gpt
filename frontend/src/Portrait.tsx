interface PortraitProps {
    imageSrc: string;
    name: string;
}

const Portrait: React.FC<PortraitProps> = ({ imageSrc, name }) => {
    return (
        <div className="flex flex-col items-center space-y-2">
            <img src={imageSrc} alt={name} className="w-48 h-48 rounded-md object-cover" />
            <p className="text-xl">{name}</p>
        </div>
    );
};

export default Portrait;

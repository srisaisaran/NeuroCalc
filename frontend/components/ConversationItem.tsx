interface Props {
  title: string;
  selected: boolean;
  onClick: () => void;
}

export default function ConversationItem({
  title,
  selected,
  onClick,
}: Props) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left px-4 py-3 rounded-lg transition
      ${
        selected
          ? "bg-blue-600 text-white"
          : "hover:bg-[#333] text-gray-300"
      }`}
    >
      💬 {title}
    </button>
  );
}
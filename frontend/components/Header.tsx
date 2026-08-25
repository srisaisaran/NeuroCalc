export default function Header() {
  return (
    <div className="h-20 border-b border-gray-700 flex items-center justify-between px-8">
      <h2 className="text-3xl font-bold">
        NeuroCalc v3.0
      </h2>

      <span className="text-gray-300">
        🌐 Local Mode
      </span>
    </div>
  );
}
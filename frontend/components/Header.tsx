export default function Header() {
  return (
    <header
      className="
        h-20
        bg-[#111113]
        border-b
        border-[#2f2f34]
        flex
        items-center
        justify-between
        px-8
      "
    >
      {/* Left */}
      <div>

        <h2
          className="
            text-2xl
            font-bold
            text-white
            tracking-tight
          "
        >
          NeuroCalc
        </h2>

        <p
          className="
            text-xs
            text-gray-500
            mt-1
          "
        >
          NeuroCalc: Think. Solve. Learn.
        </p>

      </div>

      {/* Right */}

      <div
        className="
          flex
          items-center
          gap-3
        "
      >

        <div
          className="
            w-2.5
            h-2.5
            rounded-full
            bg-green-500
            animate-pulse
          "
        />

        <span
          className="
            text-sm
            text-gray-400
          "
        >
          Local AI Connected
        </span>

      </div>

    </header>
  );
}
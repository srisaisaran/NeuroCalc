import "./globals.css";

export const metadata = {
  title: "NeuroCalc",
  description: "NeuroCalc: Think. Solve. Learn.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
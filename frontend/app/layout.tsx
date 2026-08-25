import "./globals.css";

export const metadata = {
  title: "NeuroCalc",
  description: "AI-powered calculator and intelligent assistant",
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
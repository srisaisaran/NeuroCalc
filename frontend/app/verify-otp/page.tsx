"use client";

import { useEffect, useState } from "react";

export default function VerifyOTPPage() {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // --------------------------------------------------
  // Load email from localStorage
  // --------------------------------------------------

  useEffect(() => {
    const savedEmail = localStorage.getItem("verification_email");

    if (savedEmail) {
      setEmail(savedEmail);
    }
  }, []);

  // --------------------------------------------------
  // Verify OTP
  // --------------------------------------------------

  const verifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/verify-otp",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            otp,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail);
      }

      // Remove temporary email
      localStorage.removeItem("verification_email");

      alert("🎉 Email verified successfully!");

      // Go to Login page
      window.location.href = "/";

    } catch (err) {

      if (err instanceof Error) {
        setError(err.message);
      }

    } finally {

      setLoading(false);

    }
  };

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <main
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "#f5f5f5",
      }}
    >
      <form
        onSubmit={verifyOTP}
        style={{
          width: "400px",
          background: "white",
          padding: "30px",
          borderRadius: "12px",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
          display: "flex",
          flexDirection: "column",
          gap: "15px",
        }}
      >
        <h2
          style={{
            textAlign: "center",
          }}
        >
          Verify Your Email
        </h2>

        <input
          type="email"
          value={email}
          readOnly
          placeholder="Email"
          style={{
            padding: "12px",
            fontSize: "16px",
          }}
        />

        <input
          type="text"
          placeholder="Enter 6-digit OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          maxLength={6}
          required
          style={{
            padding: "12px",
            fontSize: "16px",
          }}
        />

        {error && (
          <p
            style={{
              color: "red",
              margin: 0,
            }}
          >
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "12px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          {loading ? "Verifying..." : "Verify Email"}
        </button>
      </form>
    </main>
  );
}
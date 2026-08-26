"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Invalid email or password."
        );
      }

      localStorage.setItem(
        "neurocalc_user",
        JSON.stringify(data.user)
      );

      router.push("/chat");

    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Something went wrong.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login-page">

      <div className="background-glow glow-one" />
      <div className="background-glow glow-two" />

      <div className="login-container">

        {/* LOGO */}
        <div className="logo-wrapper">
          <div className="logo">
            🧠
          </div>
        </div>

        {/* TITLE */}
        <h1 className="login-title">
          Welcome back
        </h1>

        <p className="login-subtitle">
          Sign in to continue with{" "}
          <span>NeuroCalc</span>
        </p>

        {/* LOGIN CARD */}
        <div className="login-card">

          <form onSubmit={handleLogin}>

            {/* EMAIL */}
            <div className="input-group">

              <label htmlFor="email">
                Email
              </label>

              <div className="input-wrapper">

                <span className="input-icon">
                  ✉
                </span>

                <input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) =>
                    setEmail(e.target.value)
                  }
                  required
                />

              </div>

            </div>

            {/* PASSWORD */}
            <div className="input-group">

              <div className="password-label">

                <label htmlFor="password">
                  Password
                </label>

                <button
                  type="button"
                  className="forgot-button"
                  onClick={() =>
                    setError(
                      "Password reset will be available soon."
                    )
                  }
                >
                  Forgot password?
                </button>

              </div>

              <div className="input-wrapper">

                <span className="input-icon">
                  🔒
                </span>

                <input
                  id="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >
                  {showPassword ? "🙈" : "👁️"}
                </button>

              </div>

            </div>

            {/* ERROR */}
            {error && (
              <div className="login-error">
                <span>⚠</span>
                {error}
              </div>
            )}

            {/* LOGIN BUTTON */}
            <button
              type="submit"
              className="login-button"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner" />
                  Signing in...
                </>
              ) : (
                <>
                  Sign In
                  <span className="arrow">
                    →
                  </span>
                </>
              )}
            </button>

          </form>

          {/* DIVIDER */}
          <div className="divider">
            <span>OR</span>
          </div>

          {/* SIGNUP */}
          <p className="signup-text">
            Don't have an account?
          </p>

          <Link
            href="/signup"
            className="signup-button"
          >
            Create your NeuroCalc account
          </Link>

        </div>

        {/* FOOTER */}
        <p className="login-footer">
          🧠 NeuroCalc
          <span>•</span>
          NeuroCalc: Think. Solve. Learn.
        </p>

      </div>

    </main>
  );
}
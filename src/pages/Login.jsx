import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();

  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [signupEmail, setSignupEmail] = useState("");
  const [signupPassword, setSignupPassword] = useState("");
  const [ufid, setUfid] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    document.body.classList.add("login-page");
    document.documentElement.classList.add("login-page");

    return () => {
      document.body.classList.remove("login-page");
      document.documentElement.classList.remove("login-page");
    };
  }, []);

  async function handleLogin(e) {
    e.preventDefault();
    if (!email.endsWith("@ufl.edu")) return setError("Please use your @ufl.edu email.");
    if (!password.trim()) return setError("Password cannot be empty.");
    
    try {
    const res = await fetch("http://localhost:8000/api/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      // Get account type from backend
      localStorage.setItem("user", JSON.stringify(data));
      navigate("/explore", { replace: true });
    } else {
      setError(data.error || "Login failed");
    }
  } catch (err) {
    setError("Network error");
  }
  }

  

  async function handleSignup(e) {
    e.preventDefault();
    if (!signupEmail.endsWith("@ufl.edu")) return setError("Please use @ufl.edu email.");
    if (signupPassword.trim().length < 4) return setError("Password must be at least 4 chars.");
    
     try {
    const res = await fetch("http://localhost:8000/api/signup/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: signupEmail,
        password: signupPassword,
        ufid,
        name: signupEmail.split("@")[0], // optional default name
      }),
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("user", JSON.stringify({ email: signupEmail, ufid }));
      navigate("/explore", { replace: true });
    } else {
      setError(data.error || "Sign up failed");
    }
  } catch (err) {
    setError("Network error");
  }
  }
  

  return (
    <div className="login-wrap">
      <section className="login-card">

        <div className="tab-row">
          <button
            className={`tab-btn ${mode === "login" ? "active" : ""}`}
            onClick={() => { setMode("login"); setError(""); }}
          >
            Login
          </button>

          <button
            className={`tab-btn ${mode === "signup" ? "active" : ""}`}
            onClick={() => { setMode("signup"); setError(""); }}
          >
            Sign Up
          </button>
        </div>

        <h1 className="login-title">Club Hub</h1>

        {mode === "login" && (
          <form onSubmit={handleLogin} className="login-form">
            <div className="form-field">
              <label>Email</label>
              <input className="input" type="email" required value={email}
                onChange={(e) => setEmail(e.target.value)} />
            </div>

            <div className="form-field">
              <label>Password</label>
              <input className="input" type="password" required value={password}
                onChange={(e) => setPassword(e.target.value)} />
            </div>

            {error && <p className="error-text">{error}</p>}
            <button className="btn-primary" type="submit">Sign In</button>
          </form>
        )}

        {mode === "signup" && (
          <form onSubmit={handleSignup} className="login-form">
            <div className="form-field">
              <label>Email</label>
              <input className="input" type="email" required value={signupEmail}
                onChange={(e) => setSignupEmail(e.target.value)} />
            </div>

            <div className="form-field">
              <label>Password</label>
              <input className="input" type="password" required value={signupPassword}
                onChange={(e) => setSignupPassword(e.target.value)} />
            </div>

            <div className="form-field">
              <label>UFID</label>
              <input className="input" type="text" required value={ufid}
                onChange={(e) => setUfid(e.target.value)} />
            </div>

            {error && <p className="error-text">{error}</p>}
            <button className="btn-primary" type="submit">Create Account</button>
          </form>
        )}

      </section>
    </div>
  );
}


import { useEffect, useState  } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    document.body.classList.add("login-page");
    document.documentElement.classList.add("login-page");
  return () => {
    document.body.classList.remove("login-page");
    document.documentElement.classList.remove("login-page");
  };
  }, []);
//   async function handleSubmit(e) {
//     e.preventDefault();

//     // Simple front-end validation
//     if (!email.endsWith("@ufl.edu")) {
//       setError("Please use your @ufl.edu email address.");
//       return;
//     }
//     if (password.trim().length < 1) {
//       setError("Password cannot be empty.");
//       return;
//     }

//     try {
//       const response = await fetch("http://localhost:8000/login/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ email, password }),
//       });

//       const data = await response.json();

//       if (response.ok) {
//         // Login success
//         localStorage.setItem("user", JSON.stringify(data));
//         navigate("/explore", { replace: true });
//       } else {
//         // Login failed
//         setError(data.error || "Login failed. Please try again.");
//       }
//     } catch (err) {
//       setError("Unable to connect to the server.");
//     }
// }

    function handleSubmit(e) {
    e.preventDefault();
    // TODO: validate credentials, set auth state/token

    // Simple front-end validation
    if (!email.endsWith("@ufl.edu")) {
      setError("Please use your @ufl.edu email address.");
      return;
    }
    if (password.trim().length < 1) {
      setError("Password cannot be empty.");
      return;
    }
    // Temp login success simulation
    localStorage.setItem("user", JSON.stringify({ email })); // save to storage
    setError("");
    navigate("/explore", { replace: true }); // go to Explore after login
    }

  return (
    <div className="login-wrap">
      <section className="login-card">
      <h1 id="login-title" className="login-title">Club Hub</h1>
      <form onSubmit={handleSubmit}>
    <div className="form-field">
      <label htmlFor="email" className="field-label lg">Email</label>
        <input
          id="email"
          className="input"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
    </div>
    <div className="form-field">
      <label htmlFor="password" className="field-label">Password</label>
        <input
          id="password"
          className="input"
          type="password"
          autoComplete="current-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
    </div>

    {error && <p className="error-text">{error}</p>}
        <button type="submit" className="btn-primary">Sign in</button>
      </form>
      </section>
    </div>
  );
}


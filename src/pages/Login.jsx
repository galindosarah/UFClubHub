import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    // TODO: validate credentials, set auth state/token
    navigate("/explore", { replace: true }); // go to Explore after login
  }

  return (
    <div style={{ maxWidth: 420, margin: "4rem auto" }}>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Email
          <input type="email" required />
        </label>
        <br />
        <label>
          Password
          <input type="password" required />
        </label>
        <br />
        <button type="submit">Sign in</button>
      </form>
    </div>
  );
}

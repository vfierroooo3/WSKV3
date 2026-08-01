import { useNavigate } from "react-router-dom";
import "../components/css/Button.css"
import sharedApi from "../components/api/api";
import {useState} from "react";

function LoginPage() {
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");

  // Check login credentials
  function checkLogin() {
    const userId = document.getElementById("userId").value;
    const password = document.getElementById("password").value;
    
    if (!userId || !password) {
      setErrorMessage("Please fill in all fields!");
      return;
    }

    handleLogin(userId, password);
  }

  // Handle login
  async function handleLogin(userId, password) {
    try {
      const result = await sharedApi("/login", "POST", { userId, password });

      if (result.success) {
        localStorage.setItem("isLogin", "true");
        localStorage.setItem("userId", userId);
        navigate("/main-page");
      } else {
        setErrorMessage(result.message);
      }
    } catch (error) {
      console.error("Error during login:", error);
      setErrorMessage("An error occurred during login. Please try again.");
    }
  }
  return (
    <main style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "24px"}}>
      <h1>Login</h1>
        <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "300px"  }}>
          <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
            UserId: <input type="text" id="userId" placeholder="Please Enter UserId" />
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
            Password: <input type="password" id="password" placeholder="Please Enter Password" />
          </div>

          <span style={{ color: "red" }}>{errorMessage}</span>

          <button type="button" onClick={checkLogin} className="custom-button">
            Login
          </button>

          <div style={{ display: "flex", justifyContent: "flex-end"}}>
            <a href="/create-user">Create New User</a>
          </div>
        </div>
    </main>
  );
}

export default LoginPage;
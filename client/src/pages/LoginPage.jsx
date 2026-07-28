import { useNavigate } from "react-router-dom";
import "../components/css/Button.css"
import sharedApi from "../components/api/api";

function LoginPage() {
  const navigate = useNavigate();

  // Check login credentials
  function checkLogin() {
    const userId = document.querySelector('input[placeholder="Please Enter UserId"]').value;
    const password = document.querySelector('input[placeholder="Please Enter Password"]').value;
    const errorMessage = document.getElementById("error-message");
    
    if (!userId || !password) {
      errorMessage.innerText = "Please fill in all fields!";
      return;
    }

    handleLogin(userId, password, errorMessage);
  }

  // Handle login
  async function handleLogin(userId, password, errorMessage) {
    try {
      const result = await sharedApi("/login", "POST", { userId, password });

      if (result.success) {
        navigate("/main-page", { state: { userId: userId } });
      } else {
        errorMessage.innerText = result.message;
      }
    } catch (error) {
      console.error("Error during login:", error);
      errorMessage.innerText = "An error occurred during login. Please try again.";
    }
    }
  return (
    <main style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "24px"}}>
      <h1>Login</h1>
        <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "300px"  }}>
          <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
            UserId: <input type="text" id="user-id" placeholder="Please Enter UserId" />
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
            Password: <input type="password" id="password" placeholder="Please Enter Password" />
          </div>

          <span style={{ color: "red" }} id="error-message"></span>

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
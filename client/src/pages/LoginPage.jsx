import { useNavigate } from "react-router-dom";

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
  function handleLogin(userId, password, errorMessage) {
    // call API
    let successfulLogin = true; // Simulate API call

    if(successfulLogin){
      navigate("/main-page", { state: { userId: userId } });
    }else{
      errorMessage.innerText = "Invalid UserId or Password!";
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

          <button type="button" onClick={checkLogin}>
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
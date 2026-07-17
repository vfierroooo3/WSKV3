import { useNavigate } from "react-router-dom";

function CreateUserPage() {
    
    const navigate = useNavigate();

    // Check password validity
    function checkPassword(){
        const userId = document.getElementById("user-id").value;
        const newPassword = document.getElementById("new-password").value;
        const confirmPassword = document.getElementById("confirm-password").value;
        const errorMessage = document.getElementById("error-message");
        
        if(!userId || !newPassword || !confirmPassword){
            errorMessage.innerText = "Please fill in all fields ！";
            return;
        }

        if(newPassword !== confirmPassword){
            errorMessage.innerText = "Passwords do not match ！";
            return;
        }
        handleCreateUser(userId, newPassword, errorMessage);
    }

    // Handle user creation
    function handleCreateUser(userId, newPassword, errorMessage) {
        // Call backend API to create user
        let successfulCreation = true; // Simulate API call
        if(successfulCreation){
            alert("User created successfully！");
            navigate("/");
        }else{
            errorMessage.innerText = "User creation failed！";
        }
    }
    
    return (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "24px"}}>
            <h1>Create User</h1>
            <div style={{display: "flex", flexDirection: "column", gap: "12px", width: "300px"}}>
                <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                    New UserId: <input type="text" id="user-id" placeholder="Please Enter UserId" />
                </div>

                <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                    New Password: <input type="password" id="new-password" placeholder="Please Enter Password" />
                </div>

                <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                    Confirm Password: <input type="password" id="confirm-password" placeholder="Please Confirm Password" />
                </div>

                <span style={{ color: "red" }} id="error-message"></span>

                <button type="button" onClick={checkPassword}>
                    Create User
                </button>

                <div style={{ display: "flex", justifyContent: "flex-end"}}>
                    <a href="/">Back to Login</a>
                </div>
            </div>
        </div>
    );
}

export default CreateUserPage;
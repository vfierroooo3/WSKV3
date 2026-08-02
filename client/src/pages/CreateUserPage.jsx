import { useNavigate } from "react-router-dom";
import "../components/css/Button.css"
import sharedApi from "../components/api/api";
import {useState} from "react";

function CreateUserPage() {
    
    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState("");

    // Check password validity
    function checkPassword(){
        const userId = document.getElementById("user-id").value;
        const newPassword = document.getElementById("new-password").value;
        const confirmPassword = document.getElementById("confirm-password").value;
        
        if(!userId || !newPassword || !confirmPassword){
            setErrorMessage("Please fill in all fields ！");
            return;
        }

        if(newPassword !== confirmPassword){
            setErrorMessage("Passwords do not match ！");
            return;
        }
        handleCreateUser(userId, newPassword);
    }

    // Handle user creation
    async function handleCreateUser(userId, newPassword) {
        // Call backend API to create user
        try {
            const result = await sharedApi("/add_user", "POST", { userId, password: newPassword });

            if (result.success) {
                alert("User created successfully! Please log in.");
                navigate("/");
            } else {
                setErrorMessage(result.message);
            }
        } catch (error) {
            console.error("Error during user creation:", error);
            setErrorMessage("An error occurred during user creation. Please try again.");
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

                <span style={{ color: "red" }}>{errorMessage}</span>

                <button type="button" onClick={checkPassword} className="custom-button">
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
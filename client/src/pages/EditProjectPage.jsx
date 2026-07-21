import MainLayout from "../components/layout/MainLayout.jsx";
import { useLocation } from "react-router-dom";
function EditProjectPage() {
  const location = useLocation();
  const projectId = location.state?.projectId;

  // Edit Project
  function handleEditProject(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const projectData = Object.fromEntries(formData);
    // Call API
    const successfulCreation = true; // Simulate API call
    if (successfulCreation) {
      navigate(`/main-page`);
    }else{
      document.getElementById("error-message").innerText = "Failed to create project.";
    }
  }
  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <h1>Edit Project</h1>
        <form style={{ display: "flex", flexDirection: "column", gap: "12px", width: "300px"}} onSubmit={handleEditProject}>
          <div>
            <label>ID:</label>
            <br/>
            <input type="text" id="projectId" name="projectId" style={{width: "300px"}} value={projectId} readOnly/>
          </div>
          <div>
            <label>Name:</label>
            <br/>
            <input type="text" id="projectName" name="projectName" required style={{width: "300px"}} />
          </div>
          <div>
            <label>Description:</label>
            <br/>
            <textarea id="projectDescription" name="projectDescription" required style={{width: "300px", height: "100px"}} />
          </div>
          <button type="submit">Edit Project</button>
        </form>
        <span id="error-message" style={{ color: "red" }}></span>
      </div>
    </MainLayout>
  );
}

export default EditProjectPage;
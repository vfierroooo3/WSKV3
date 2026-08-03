import { useEffect, useState } from "react";
import MainLayout from "../components/layout/MainLayout.jsx";
import MyProjectTable from "../components/table/MyProjectTable.jsx";
import NavigateButton from "../components/button/NavigateButton.jsx";
import sharedApi from "../components/api/api";

function MainPage() {
  const userId = localStorage.getItem("userId");

  // State to hold project lists
  const [myProjectsList, setMyProjectsList] = useState([]);

  // Get my projects List
  async function getMyProjects(userId){
    try {
      const result = await sharedApi("/get_user_projects_list", "POST", { userId });
      if (result.success) {
        setMyProjectsList(result.projects);
      } else {
        setErrorMessage(result.message);
      }
    } catch (error) {
      console.error("Error during get my projects:", error);
      setErrorMessage("An error from server occurred.");
    }
  }

  // Execute when component rendering
  useEffect(() => {
    getMyProjects(userId);
  }, [userId]);

  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <div>
          <h1>My Projects</h1>
          <MyProjectTable 
            projects={myProjectsList} 
          />
          <br/>
          <div className="button-container">
            <NavigateButton text="Create New Project" destination="/create-project"/>
            <NavigateButton text="Join Existing Project" destination="/join-project"/>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

export default MainPage;
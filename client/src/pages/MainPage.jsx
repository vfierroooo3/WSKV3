import { useEffect, useState } from "react";
import MainLayout from "../components/layout/MainLayout.jsx";
import MyProjectTable from "../components/table/MyProjectTable.jsx";
import NavigateButton from "../components/button/NavigateButton.jsx"

function MainPage() {
  const userId = localStorage.getItem("userId");

  // State to hold project lists
  const [myProjectsList, setMyProjectsList] = useState([]);

  // Get my projects List
  function getMyProjects(userId){
    // Simulate API call
    const result = [
        {
        id: 1,
        name: "Project Alpha"
      },
      {
        id: 2,
        name: "Project Beta"
      },
      {
        id: 3,
        name: "Project Gamma"
      },
    ];
    // put the result into state
    setMyProjectsList(result);
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
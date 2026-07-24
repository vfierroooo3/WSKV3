import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout.jsx";
import MyProjectTable from "../components/table/MyProjectTable.jsx";
import NavigateButton from "../components/button/NavigateButton.jsx"

function MainPage() {
  const navigate = useNavigate();

  // Get user ID from location state
  const location = useLocation();
  const userId = location.state?.userId;
  
  // State to hold project lists
  const [myProjectsList, setMyProjectsList] = useState([]);

  // State to hold other projects
  const [otherProjectsList, setOtherProjectsList] = useState([]);

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

  // Get other projects List
  function getOtherProjects(userId){
    const result = [
      {
        id: 4,
        name: "Project Delta",
        join: false
      },
      {
        id: 5,
        name: "Project Epsilon",
        join: true
      },
      {
        id: 6,
        name: "Project Zeta",
        join: true
      },
    ];
    setOtherProjectsList(result);
  }

  // Execute when component rendering
  useEffect(() => {
    getMyProjects(userId);
    getOtherProjects(userId);
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
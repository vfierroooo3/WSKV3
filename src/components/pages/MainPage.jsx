import { useNavigate } from "react-router-dom";
import MainLayout from "../layout/MainLayout.jsx";
import MyProjectTable from "../table/MyProjectTable.jsx";
import OtherProjectTable from "../table/OtherProjectTable.jsx";

function MainPage() {
  const navigate = useNavigate();
  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center"}}>
            <h1>My Projects</h1>
            <button type="button" onClick={() => navigate("/create-project")} style={{height: "30px"}}>Create New Project</button>
          </div>
          <MyProjectTable />
        </div>
      </div>
      <br/>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <div>
          <h1>Other Projects</h1>
          <OtherProjectTable />
        </div>
      </div>
    </MainLayout>
  );
}

export default MainPage;
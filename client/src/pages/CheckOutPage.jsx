import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "../components/css/Button.css"
import MainLayout from "../components/layout/MainLayout.jsx";
import CheckOutTable from "../components/table/CheckOutTable.jsx";
import sharedApi from "../components/api/api.jsx";

function CheckOutPage() {
  // Get project ID from location state
  const location = useLocation();
  const projectId = location.state?.projectId;
  const projectName = location.state?.projectName;
  
  // hardware list parameters
  const [hardwaresList, setHardwaresList] = useState([]);

  // Check out items parameters
  const [checkOutItems, setCheckOutItems] = useState([]);

  const [errorMessage, setErrorMessage] = useState("");
  // Get hardware list from API
  async function getHardwareList() {
    try{
      const result = await sharedApi(
        "/get_hw_info", 
        "GET"
      );
      setHardwaresList(result.HardwareSets);
    } catch (error) {
      console.error(error);
    }
  }

  // Check out items change handler
  function handleTableChange(items) {
    setCheckOutItems(items);
  }

  // Check out items submit handler
  async function handleCheckOut(event) {
    event.preventDefault();
    try {
      const results = await Promise.all(
        checkOutItems.map((item) =>
          sharedApi(
            "/check_out",
            "POST",
            {
              projectId: projectId,
              hwSetName: item.hwName,
              qty: item.requestQuantity
            }
          )
        )
      );

      const hasFailed = results.some((result) => !result.success);

      if (hasFailed) {
        setErrorMessage("Some items failed to check out.");
      } else {
        alert("All items checked out successfully!");
        getHardwareList();
      }

    } catch (error) {
      setErrorMessage("An error occurred while checking out the items.");
    }
  }

  // Execute when component rendering
  useEffect(() => {
    getHardwareList();
  }, [])

  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <h1>Check Out Resources</h1>
        <form onSubmit={handleCheckOut}>
          <h3>Project ID: {projectId}</h3>
          <h3>Project Name: {projectName}</h3>
          <CheckOutTable
            hardwaresList={hardwaresList} // Pass hardware list to table
            onDataChange={handleTableChange} // Handle data change from table
          />
          <span style={{ color: "red" }}>{errorMessage}</span>
          <button type="submit" className="custom-button">Check Out</button>
        </form>
      </div>
    </MainLayout>
  );
}

export default CheckOutPage;
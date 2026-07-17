import { useState } from "react";
import { useNavigate } from "react-router-dom";
import MainLayout from "../layout/MainLayout.jsx";
import CheckInTable from "../table/CheckInTable.jsx";

function CheckInPage() {
  const navigate = useNavigate();
  const [checkInItems, setCheckInItems] = useState([]);
  const hardwares = [
    {
      id: 1,
      name: "ABC",
      capacity: 1200,
      available: 1200,
    },
    {
      id: 2,
      name: "DEF",
      capacity: 850,
      available: 850,
    }
  ];

  function handleTableChange(items) {
    setCheckInItems(items);
  }

  function handleCheckIn(event) {
    event.preventDefault()
    console.log("Check-in data:", checkInItems);
  }

  return (
    <MainLayout>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
        <h1>Check In</h1>
        <form onSubmit={handleCheckIn}>
          <CheckInTable 
            hardwares={hardwares}
            onDataChange={handleTableChange}
          />
          <button type="submit" style={{ width: "100%"}}>Check In</button>
        </form>
      </div>
    </MainLayout>
  );
}

export default CheckInPage;
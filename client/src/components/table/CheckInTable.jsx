import { useState } from "react";
import "../css/Table.css";
function CheckInTable({hardwaresList, onDataChange}) {
  // List of requests parameter
  const [requests, setRequests] = useState({});

  // Handle request change
  function handleRequestChange(hardwareName, value) {
    const quantity = Number(value); // Convert input value to number

    // Update requests state
    const updatedRequests = {
      ...requests, // Keep existing requests
      [hardwareName]: quantity, // Update quantity for the specific hardware
    };

    // update requests parameter
    setRequests(updatedRequests);

    // Update selected items (only with a request quantity)
    const selectedItems = Object.entries(hardwaresList)
    .map(([name, checkedOut]) => ({
      hwName: name,
      checkedOut: checkedOut,
      requestQuantity: updatedRequests[name] ?? 0,
    }))
    .filter((item) => item.requestQuantity > 0);

    onDataChange(selectedItems);
  }
  return (
    <div style={{width: "100%",maxWidth: "900px", margin: "24px auto",  overflowX: "auto" }} >
      <table className="check-table">
        <thead>
          <tr>
            <th className="check-table-header">Hardware Name</th>
            <th className="check-table-header">Checked Out</th>
            <th className="check-table-header">Return</th>
          </tr>
        </thead>

        <tbody>
          {Object.entries(hardwaresList).map(([hardwareName, checkedOut]) => (
            <tr key={hardwareName}>
              <td className="check-table-cell">
                {hardwareName}
              </td>

              <td className="check-table-cell">
                {checkedOut.toLocaleString()}
              </td>

              <td className="check-table-cell">
                <input
                  type="number"
                  min="0"
                  max={checkedOut}
                  value={requests[hardwareName] ?? ""}
                  onChange={(event) =>
                    handleRequestChange(
                      hardwareName,
                      event.target.value
                    )
                  }
                  style={{ width: "100%" }}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CheckInTable;
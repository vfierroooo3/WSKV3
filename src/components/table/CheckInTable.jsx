import { useState } from "react";
function CheckInTable({hardwares, onDataChange}) {
  const [requests, setRequests] = useState({});

function handleRequestChange(hardware, value) {
    const quantity = Number(value);

    const updatedRequests = {
      ...requests,
      [hardware.id]: quantity,
    };

    setRequests(updatedRequests);

    const selectedItems = hardwares
      .map((item) => ({
        ...item,
        requestQuantity: updatedRequests[item.id] ?? 0,
      }))
      .filter((item) => item.requestQuantity > 0);

    onDataChange(selectedItems);
  }

  const tableStyle = {
    width: "100%",
    borderCollapse: "collapse",
    backgroundColor: "#ffffff",
  };

  const headerStyle = {
    padding: "12px",
    border: "1px solid #dddddd",
    backgroundColor: "#f3f4f6",
    textAlign: "left",
  };

  const cellStyle = {
    padding: "12px",
    border: "1px solid #dddddd",
    textAlign: "left",
  };

  return (
    <div
      style={{
        width: "100%",
        maxWidth: "900px",
        margin: "24px auto",
        overflowX: "auto",
      }}
    >
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={headerStyle}>Hardware Name</th>
            <th style={headerStyle}>Capacity</th>
            <th style={headerStyle}>Available</th>
            <th style={headerStyle}>Request</th>
          </tr>
        </thead>

        <tbody>
          {hardwares.map((hardware) => (
            <tr key={hardware.name}>
              <td style={cellStyle}>{hardware.name}</td>
              <td style={cellStyle}>
                {hardware.capacity.toLocaleString()}
              </td>
              <td style={cellStyle}>{hardware.available.toLocaleString()}</td>
              <td style={cellStyle}>
                <input
                  type="number"
                  min="0"
                  max={hardware.available}
                  value={requests[hardware.id]}
                  onChange={(event) =>
                    handleRequestChange(hardware, event.target.value)
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
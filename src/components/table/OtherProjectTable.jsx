import { useNavigate } from "react-router-dom";
import "../css/Table.css";

function ProjectTable({ projects }) {

  const navigate = useNavigate();

  return (
    <div style={{ width: "100%", maxWidth: "900px", overflowX: "auto" }}>
      <table className="project-table">
        <thead>
          <tr>
            <th className="project-table-header">Project ID</th>
            <th className="project-table-header">Project Name</th>
            <th className="project-table-header">Action</th>
          </tr>
        </thead>

        <tbody>
          {projects.map((project) => (
            <tr key={project.id}>
              <td className="project-table-cell">{project.id}</td>
              <td className="project-table-cell">{project.name}</td>
              <td>
                {project.join ? (
                  <div className="project-table-cell" style={{ display: "flex", gap: "10px" }}>
                    <button type="button" onClick={() => navigate('/check-out', { state: { projectId: project.id } })}>
                      Check Out
                    </button>
                    <button type="button" onClick={() => navigate('/check-in', { state: { projectId: project.id } })}>
                      Check In
                    </button>
                  </div>
                ) : (
                  <div className="project-table-cell" style={{ display: "flex", gap: "10px" }}>
                    <button type="button" style={{ width: "100%" }}>
                      Join Project
                    </button>
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProjectTable;
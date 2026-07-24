import { Link } from "react-router-dom";

function Header() {

  return (
    <header
      style={{
        height: "60px",
        borderBottom: "1px solid #000000",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 24px",
      }}
    >
      <h2>ADVANCED PROG AND APP DEV I | Team Project 3</h2>

      <div style={{display: "flex", gap: "16px"}}>
        <Link to="/main-page">Projects</Link>

        <Link to="/">Log out</Link>
      </div>
    </header>
  );
}
export default Header;
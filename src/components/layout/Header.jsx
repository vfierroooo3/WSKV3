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

    <nav style={{ display: "flex", gap: "16px" }}>
      <a href="/main-page">Projects</a>
      <a href="/check-in">Check In</a>
      <a href="/check-out">Check Out</a>
    </nav>
    </header>
  );
}
export default Header;
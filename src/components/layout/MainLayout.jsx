import Header from "./Header";

function MainLayout({ children }) {
  return (
    <div>
      <Header />

      <main
        style={{
          padding: "24px",
        }}
      >
        {children}
      </main>
    </div>
  );
}

export default MainLayout;
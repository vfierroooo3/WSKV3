import Header from "./Header";

function MainLayout({ children }) {
  return (
    <>
      <Header />

      <main
        style={{
          padding: "24px",
        }}
      >
        {children}
      </main>
    </>
  );
}

export default MainLayout;
export default function Navbar({ title }) {
  return (
    <header className="dashboard-navbar">
      <div className="nav-brand">
        <h1>{title}</h1>
        <div className="badge ai-badge">AI Powered</div>
      </div>
      <div className="nav-actions">
        <button className="btn btn-outline" title="Reset view">↺ Reset</button>
        <div className="user-profile">Admin</div>
      </div>
    </header>
  );
}

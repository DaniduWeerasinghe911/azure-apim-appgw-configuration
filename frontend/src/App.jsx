import React from "react";
import { MsalProvider } from "@azure/msal-react";
import { msalInstance, msalInitialized } from "./msal";
import Dashboard from "./Dashboard";

function App() {
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => {
    msalInitialized.then(() => setReady(true));
  }, []);
  if (!ready) return <div>Loading authentication...</div>;
  return (
    <MsalProvider instance={msalInstance}>
      <Dashboard />
    </MsalProvider>
  );
}

export default App;

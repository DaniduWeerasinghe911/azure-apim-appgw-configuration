import React from "react";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "./authConfig";

const apiBase = "http://localhost:8000";

function Dashboard() {
  const { instance, accounts } = useMsal();
  const [costs, setCosts] = React.useState(null);
  const [idleVMs, setIdleVMs] = React.useState(null);
  const [disks, setDisks] = React.useState(null);
  const [summary, setSummary] = React.useState("");
  const [error, setError] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    if (accounts && accounts.length > 0) {
      instance.setActiveAccount(accounts[0]);
    }
  }, [accounts, instance]);

  const getToken = async () => {
    if (!accounts || accounts.length === 0)
      throw new Error("Please sign in first.");
    const response = await instance.acquireTokenSilent({
      ...loginRequest,
      account: accounts[0],
    });
    return response.accessToken;
  };

  const handleLogin = () => {
    instance.loginPopup(loginRequest);
  };

  const fetchData = async () => {
    setLoading(true);
    setError("");
    try {
      const token = await getToken();
      const headers = { Authorization: `Bearer ${token}` };
      const [costsRes, vmsRes, disksRes] = await Promise.all([
        fetch(`${apiBase}/costs`, { headers }),
        fetch(`${apiBase}/idle-vms`, { headers }),
        fetch(`${apiBase}/unattached-disks`, { headers }),
      ]);
      if (!costsRes.ok || !vmsRes.ok || !disksRes.ok) {
        throw new Error("One or more API calls failed");
      }
      setCosts(await costsRes.json());
      setIdleVMs((await vmsRes.json()).idle_vms);
      setDisks((await disksRes.json()).unattached_disks);
    } catch (err) {
      setError(err.message);
      setCosts(null);
      setIdleVMs(null);
      setDisks(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchSummary = async () => {
    setError("");
    try {
      const token = await getToken();
      const headers = {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      };
      const body = JSON.stringify({ costs, idleVMs, disks });
      const res = await fetch(`${apiBase}/insight-summary`, {
        method: "POST",
        headers,
        body,
      });
      if (!res.ok) throw new Error("Failed to fetch summary");
      const data = await res.json();
      setSummary(data.summary);
    } catch (err) {
      setError(err.message);
      setSummary("");
    }
  };

  React.useEffect(() => {
    if (accounts && accounts.length > 0) {
      fetchData();
    }
    // eslint-disable-next-line
  }, [accounts]);

  if (!accounts || accounts.length === 0) {
    return (
      <div style={{ padding: 32 }}>
        <h1>Azure Cost Optimizer Dashboard</h1>
        <button onClick={handleLogin}>Sign in with Azure AD</button>
        {error && <div style={{ color: "red" }}>Error: {error}</div>}
      </div>
    );
  }

  return (
    <div style={{ padding: 32 }}>
      <h1>Azure Cost Optimizer Dashboard</h1>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: "red" }}>Error: {error}</div>}
      <button onClick={fetchData}>Refresh Data</button>
      <div>
        <h2>Current Spend</h2>
        <pre>{JSON.stringify(costs, null, 2)}</pre>
      </div>
      <div>
        <h2>Idle VMs</h2>
        <pre>{JSON.stringify(idleVMs, null, 2)}</pre>
      </div>
      <div>
        <h2>Unattached Disks</h2>
        <pre>{JSON.stringify(disks, null, 2)}</pre>
      </div>
      <div>
        <button onClick={fetchSummary}>Generate AI Summary</button>
        <h2>AI Cost Optimization Summary</h2>
        <pre>{summary}</pre>
      </div>
    </div>
  );
}

export default Dashboard;

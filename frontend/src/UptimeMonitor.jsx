import React, { useEffect, useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export default function UptimeMonitor() {
  const [urls, setUrls] = useState([]);
  const [newUrl, setNewUrl] = useState("");
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");

  const fetchStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/status`);

      setUrls(response.data);

      setLastUpdated(
        new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );

      setError("");
    } catch (err) {
      console.error("Failed to fetch status:", err);
    }
  };

  useEffect(() => {
    fetchStatus();

    const interval = setInterval(fetchStatus, 10000);

    return () => clearInterval(interval);
  }, []);

  const handleAddUrl = async (e) => {
    e.preventDefault();

    if (!newUrl.trim()) return;

    try {
      await axios.post(`${API_BASE_URL}/urls`, {
        url: newUrl.trim(),
      });

      setNewUrl("");

      fetchStatus();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to add URL.");
    }
  };

  const total = urls.length;
  const healthy = urls.filter((u) => u.status === "UP").length;
  const restricted = urls.filter((u) => u.status === "RESTRICTED").length;
  const down = urls.filter((u) => u.status === "DOWN").length;

  return (
    <div className="app">
      <header className="header">
        <div className="logo-box">
          <div className="logo-circle">⚡</div>

          <div className="title">
            <h1>Uptime Monitor</h1>
            <p>Infrastructure Health Dashboard</p>
          </div>
        </div>

        <div
          style={{
            textAlign: "right",
          }}
        >
          <div
            style={{
              color: "#22c55e",
              fontWeight: 600,
              marginBottom: 6,
            }}
          >
            ● Live Monitoring
          </div>

          <small
            style={{
              color: "#94a3b8",
            }}
          >
            Last Updated: {lastUpdated || "--:--:--"}
          </small>
        </div>
      </header>

      <div className="stats">
        <div className="stat">
          <h2>{total}</h2>
          <span>Total URLs</span>
        </div>

        <div className="stat">
          <h2>{healthy}</h2>
          <span>Healthy</span>
        </div>

        <div className="stat">
          <h2>{restricted}</h2>
          <span>Restricted</span>
        </div>

        <div className="stat">
          <h2>{down}</h2>
          <span>Down</span>
        </div>
      </div>

      <div className="add-card">
        <form
          onSubmit={handleAddUrl}
          className="input-group"
        >
          <input
            type="url"
            placeholder="https://example.com"
            value={newUrl}
            onChange={(e) => setNewUrl(e.target.value)}
            required
          />

          <button type="submit">
            Add URL
          </button>
        </form>

        {error && (
          <p
            style={{
              marginTop: 14,
              color: "#ef4444",
              fontWeight: 600,
            }}
          >
            {error}
          </p>
        )}
      </div>

      <div className="urls">
        {urls.length === 0 ? (
          <div className="url-card">
            <div className="url-info">
              <h3>No monitored URLs</h3>
              <small>Add your first website above.</small>
            </div>
          </div>
        ) : (
          urls.map((item, index) => {
            let badge = "🟢";
            let badgeClass = "badge up";

            switch (item.status) {
              case "UP":
                badge = "🟢";
                badgeClass = "badge up";
                break;

              case "RESTRICTED":
                badge = "🟠";
                badgeClass = "badge";
                break;

              case "DOWN":
                badge = "🔴";
                badgeClass = "badge down";
                break;

              default:
                badge = "🟡";
                badgeClass = "badge";
            }

            return (
              <div
                className="url-card"
                key={index}
              >
                <div className="url-info">
                  <h3>{item.url}</h3>

                  <small>
                    HTTP {item.status_code ?? "--"}
                  </small>
                </div>

                <div className="status">
                  <span className={badgeClass}>
                    {badge} {item.status}
                  </span>

                  <span className="response">
                    {item.response_time !== null
                      ? `${item.response_time} ms`
                      : "Timeout"}
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>

      <footer className="footer">
        <strong>Refresh Interval:</strong> 10 seconds &nbsp;•&nbsp;
        <strong>Backend Health Checks:</strong> Every 60 seconds
      </footer>
    </div>
  );
}
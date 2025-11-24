import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { BarChart, Clock, MessageSquare, Zap } from 'lucide-react';

const Dashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        const headers = { Authorization: `Bearer ${token}` };
        
        const [analyticsRes, metricsRes] = await Promise.all([
          axios.get('http://localhost:5000/api/analytics', { headers }),
          axios.get('http://localhost:5000/api/metrics', { headers })
        ]);
        
        setAnalytics(analyticsRes.data);
        setMetrics(metricsRes.data);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="dashboard-container flex justify-center items-center text-primary">Loading Analytics...</div>;
  }

  return (
    <div className="dashboard-container">
      <div style={{ marginBottom: '2rem' }}>
        <h1 className="text-3xl font-display font-bold mb-2">COMMAND CENTER</h1>
        <p className="text-gray-400" style={{ color: '#888' }}>System Analytics & Performance Metrics</p>
      </div>

      {/* Overview Cards */}
      <div className="grid-4">
        <StatCard 
          icon={<MessageSquare className="w-6 h-6 text-primary" />}
          label="Total Queries"
          value={analytics?.total_queries || 0}
        />
        <StatCard 
          icon={<Clock className="w-6 h-6 text-secondary" />}
          label="Avg Response Time"
          value={`${Math.round(analytics?.avg_response_time || 0)}ms`}
        />
        <StatCard 
          icon={<Zap className="w-6 h-6 text-accent" />}
          label="Success Rate"
          value="98.5%"
        />
        <StatCard 
          icon={<BarChart className="w-6 h-6 text-orange-400" style={{ color: 'orange' }} />}
          label="Active Sessions"
          value="1"
        />
      </div>

      {/* Detailed Metrics */}
      <div className="grid-2">
        {/* Intent Distribution */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 className="text-xl font-display mb-6 border-b border-[var(--glass-border)] pb-2" style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.5rem', marginBottom: '1.5rem' }}>INTENT DISTRIBUTION</h3>
          <div className="space-y-4" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {analytics?.intent_distribution && Object.entries(analytics.intent_distribution).map(([intent, count]) => (
              <div key={intent} className="flex items-center gap-4">
                <div className="w-32 text-sm text-gray-400 truncate" style={{ width: '8rem', color: '#888' }}>{intent}</div>
                <div className="flex-1 h-2 bg-[var(--glass-border)] rounded-full overflow-hidden" style={{ flex: 1, height: '0.5rem', background: 'var(--glass-border)', borderRadius: '999px', overflow: 'hidden' }}>
                  <div 
                    className="h-full bg-[var(--primary-color)]"
                    style={{ width: `${(count / analytics.total_queries) * 100}%`, height: '100%', background: 'var(--primary-color)' }}
                  ></div>
                </div>
                <div className="w-12 text-right text-sm font-mono" style={{ width: '3rem', textAlign: 'right', fontFamily: 'monospace' }}>{count}</div>
              </div>
            ))}
            {!analytics?.intent_distribution && <div className="text-gray-500">No data available</div>}
          </div>
        </div>

        {/* Recent Activity (Placeholder or History) */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 className="text-xl font-display mb-6 border-b border-[var(--glass-border)] pb-2" style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.5rem', marginBottom: '1.5rem' }}>SYSTEM LOGS</h3>
          <div className="space-y-4 font-mono text-sm h-64 overflow-y-auto pr-2" style={{ fontFamily: 'monospace', fontSize: '0.875rem', height: '16rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
             <div className="flex justify-between text-gray-400" style={{ display: 'flex', justifyContent: 'space-between', color: '#888' }}>
               <span>[SYSTEM]</span>
               <span>Initialized</span>
             </div>
             <div className="flex justify-between text-[var(--primary-color)]" style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--primary-color)' }}>
               <span>[AUTH]</span>
               <span>User {user?.username} logged in</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value }) => (
  <div className="glass-panel flex items-center gap-4 hover:border-[var(--primary-color)] transition-colors group" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem', transition: 'border-color 0.3s' }}>
    <div className="p-3 rounded-lg bg-[var(--glass-border)] group-hover:bg-[var(--primary-color)]/10 transition-colors" style={{ padding: '0.75rem', borderRadius: '0.5rem', background: 'var(--glass-border)' }}>
      {icon}
    </div>
    <div>
      <div className="text-sm text-gray-400" style={{ fontSize: '0.875rem', color: '#888' }}>{label}</div>
      <div className="text-2xl font-display font-bold" style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{value}</div>
    </div>
  </div>
);

export default Dashboard;

import { AreaChart, Area, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
import { api } from '../lib/api';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from '../context/AuthContext';

const dummy = [
  { wk: 'W-1', h: 2 },
  { wk: 'W-2', h: 4 },
  { wk: 'W-3', h: 6 },
  { wk: 'W-4', h: 5 },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const { data: matches } = useQuery({
    queryKey: ['matches'],
    queryFn: () => api.get('match/me').text(),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Welcome back, {user?.email}</h1>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl p-4 card-shadow">
          <h3 className="text-sm text-gray-500">Matches</h3>
          <p className="text-3xl font-bold mt-2">{matches ? '20+' : '…'}</p>
        </div>

        <div className="bg-white rounded-2xl p-4 card-shadow">
          <h3 className="text-sm text-gray-500">Hours served</h3>
          <p className="text-3xl font-bold mt-2">42</p>
        </div>

        <div className="bg-white rounded-2xl p-4 card-shadow">
          <h3 className="text-sm text-gray-500">Upcoming gigs</h3>
          <p className="text-3xl font-bold mt-2">3</p>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-4 card-shadow">
        <h3 className="mb-4 font-medium">Weekly volunteering hours</h3>
        <AreaChart width={600} height={250} data={dummy}>
          <defs>
            <linearGradient id="colorH" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#087ea4" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#087ea4" stopOpacity={0} />
            </linearGradient>
          </defs>
          <Area type="monotone" dataKey="h" stroke="#087ea4" fill="url(#colorH)" />
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="wk" />
          <YAxis />
          <Tooltip />
        </AreaChart>
      </div>
    </div>
  );
}

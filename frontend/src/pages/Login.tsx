import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { Card, CardContent } from '../components/ui/card';

interface LoginForm {
  email: string;
  password: string;
}

export default function Login() {
  const { register, handleSubmit } = useForm<LoginForm>();
  const navigate = useNavigate();

  async function onSubmit(data: LoginForm) {
    const res = await api.post('auth/login', { json: data }).json<{ access_token: string }>();
    localStorage.setItem('token', res.access_token);
    navigate('/dashboard');
  }

  return (
    <div className="h-full flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md card-shadow">
        <CardContent className="p-6 space-y-4">
          <h2 className="text-2xl font-semibold text-center">Login</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <input
              {...register('email', { required: true })}
              placeholder="Email"
              type="email"
              className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-brand focus:ring-brand"
            />
            <input
              {...register('password', { required: true })}
              placeholder="Password"
              type="password"
              className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-brand focus:ring-brand"
            />
            <button className="w-full rounded-md bg-brand px-4 py-2 font-medium text-white hover:bg-brand-dark focus:outline-none focus:ring-2 focus:ring-brand">
              Sign in
            </button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

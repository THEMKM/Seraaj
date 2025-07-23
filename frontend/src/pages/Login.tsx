import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { Card, CardContent } from '../components/ui/card';
import FormField from '../components/FormField';

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
            <FormField label="Email">
              <input
                id="login-email"
                {...register('email', { required: true })}
                placeholder="Email"
                type="email"
                className="input input-bordered w-full"
              />
            </FormField>
            <FormField label="Password">
              <input
                id="login-password"
                {...register('password', { required: true })}
                placeholder="Password"
                type="password"
                className="input input-bordered w-full"
              />
            </FormField>
            <button className="btn btn-primary w-full">Sign in</button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

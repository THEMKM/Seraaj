import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { Card, CardContent } from '../components/ui/card';

interface SignupForm {
  email: string;
  password: string;
}

export default function Signup() {
  const { register, handleSubmit } = useForm<SignupForm>();
  const navigate = useNavigate();

  async function onSubmit(data: SignupForm) {
    await api.post('auth/register', { json: { ...data, role: 'VOLUNTEER' } });
    navigate('/login');
  }

  return (
    <div className="h-full flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md card-shadow">
        <CardContent className="p-6 space-y-4">
          <h2 className="text-2xl font-semibold text-center">Sign up</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <input
              {...register('email', { required: true })}
              placeholder="Email"
              type="email"
              className="input input-bordered w-full"
            />
            <input
              {...register('password', { required: true })}
              placeholder="Password"
              type="password"
              className="input input-bordered w-full"
            />
            <button className="btn btn-primary w-full">Create account</button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

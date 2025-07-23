import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <main className="flex min-h-screen flex-col bg-white">
      <section className="flex flex-col items-center justify-center bg-ai-gradient text-white text-center py-20 px-4">
        <h1 className="mb-4 text-5xl font-bold">Light the Way for Change</h1>
        <p className="mb-8 max-w-2xl text-lg">
          Connect with vetted volunteer opportunities—instant apply, instant impact.
        </p>
        <div className="flex gap-4">
          <Link
            to="/signup"
            className="rounded-2xl bg-white px-6 py-3 font-semibold text-brand shadow-md hover:bg-brand-light focus:outline-none focus:ring-2 focus:ring-white"
          >
            Sign Up
          </Link>
          <Link
            to="/login"
            className="rounded-2xl border border-white px-6 py-3 font-semibold text-white hover:bg-white hover:text-brand focus:outline-none focus:ring-2 focus:ring-white"
          >
            Log In
          </Link>
        </div>
      </section>
      <section className="grid gap-8 p-8 text-center md:grid-cols-3">
        <div className="flex flex-col items-center">
          <svg
            className="mb-2 h-10 w-10 text-brand-dark"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M4 4h16v2H4zm0 4h10v2H4zm0 4h16v2H4zm0 4h10v2H4z" />
          </svg>
          <h3 className="mb-1 font-semibold">Build Your Profile Once</h3>
          <p className="text-sm text-gray-600">Reuse it for all applications.</p>
        </div>
        <div className="flex flex-col items-center">
          <svg
            className="mb-2 h-10 w-10 text-brand-dark"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M13 2l-2 2h-5a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2v-5l2-2-7-7z" />
          </svg>
          <h3 className="mb-1 font-semibold">1-Click Apply</h3>
          <p className="text-sm text-gray-600">Save time with quick applications.</p>
        </div>
        <div className="flex flex-col items-center">
          <svg
            className="mb-2 h-10 w-10 text-brand-dark"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 2.5-7.5L2 9h7z" />
          </svg>
          <h3 className="mb-1 font-semibold">Instant Recognition</h3>
          <p className="text-sm text-gray-600">Share your impact on social media.</p>
        </div>
      </section>
      <footer className="mt-auto bg-gray-100 py-4 text-center text-sm">
        <nav className="space-x-4">
          <a href="/terms" className="hover:underline">Terms</a>
          <a href="/privacy" className="hover:underline">Privacy</a>
          <a href="https://github.com/example/seraaj" className="hover:underline">GitHub</a>
          <a href="/contact" className="hover:underline">Contact</a>
        </nav>
      </footer>
    </main>
  );
}

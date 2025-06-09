export default function Landing() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-brand text-white text-center p-8">
      <h1 className="text-4xl font-bold mb-4">Welcome to Seraaj</h1>
      <p className="mb-6 max-w-md text-lg">
        Connecting passionate volunteers with organizations that make a difference.
      </p>
      <a
        href="/dashboard"
        className="rounded bg-white px-6 py-3 font-semibold text-brand hover:bg-brand-light focus:outline-none focus:ring-2 focus:ring-white"
      >
        Enter Dashboard
      </a>
    </main>
  );
}

import { Footer } from "./Footer";
import { Header } from "./Header";

export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Header />
      <main className="shell">{children}</main>
      <Footer />
    </>
  );
}

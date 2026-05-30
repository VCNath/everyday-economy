import Link from "next/link";

type ButtonProps = {
  children: React.ReactNode;
  href?: string;
  variant?: "primary" | "secondary" | "ghost";
};

export function Button({ children, href, variant = "secondary" }: ButtonProps) {
  const className = `button ${variant === "primary" ? "primary" : ""} ${variant === "ghost" ? "ghost" : ""}`;
  if (href) return <Link className={className} href={href}>{children}</Link>;
  return <button className={className} type="button">{children}</button>;
}

import { ButtonHTMLAttributes } from "react";

type Variant = "primary" | "secondary" | "ghost";

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const styles: Record<Variant, string> = {
  primary: "bg-brand text-white hover:bg-brand-dark",
  secondary: "bg-slate-200 text-slate-800 hover:bg-slate-300",
  ghost: "bg-transparent text-brand hover:bg-slate-100",
};

export default function Button({ variant = "primary", className = "", ...rest }: Props) {
  return (
    <button
      className={`rounded-lg px-4 py-2 text-sm font-medium disabled:opacity-50 ${styles[variant]} ${className}`}
      {...rest}
    />
  );
}

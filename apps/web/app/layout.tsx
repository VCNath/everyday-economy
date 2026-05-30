import type { Metadata } from "next";
import { AuthProvider } from "@/components/auth/AuthProvider";
import { BetaBanner } from "@/components/beta/BetaBanner";
import { FeedbackWidget } from "@/components/beta/FeedbackWidget";
import { AppThemeProvider } from "@/components/theme/AppThemeProvider";
import "./globals.css";

export const metadata: Metadata = {
  title: "Everyday Economy",
  description: "Map-first Canadian cost-of-living dashboard"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppThemeProvider>
          <AuthProvider>
            <BetaBanner />
            {children}
            <FeedbackWidget />
          </AuthProvider>
        </AppThemeProvider>
      </body>
    </html>
  );
}

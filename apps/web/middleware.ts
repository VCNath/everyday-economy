import { NextResponse, type NextRequest } from "next/server";

const authRequired = ["/account"];
const adminRequired = ["/admin"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const authEnabled = false;

  if (!authEnabled && [...authRequired, ...adminRequired].some((prefix) => pathname.startsWith(prefix))) {
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/account/:path*", "/admin/:path*"]
};
